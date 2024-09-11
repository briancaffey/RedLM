import base64
from io import BytesIO
import requests

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image

from llama_index.core.llms import ChatMessage

from .rag import get_qa_query_engine, get_q_and_a_query_engine


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str

class QAQueryResponse(BaseModel):
    response: str

class MutliModalRequest(BaseModel):
    prompt: str
    image: str


@app.on_event("startup")
async def startup_event():
    global query_engine, q_and_a_engine
    query_engine = get_qa_query_engine()
    q_and_a_engine = get_q_and_a_query_engine()



@app.post("/query", response_model=QueryResponse)
async def perform_query(request: QueryRequest):
    """
    This endpoint is used by the evaluation script
    """

    response = query_engine.query(request.query)
    return QueryResponse(response=str(response))

@app.post("/q-and-a", response_model=QueryResponse)
async def perform_q_and_a(request: QueryRequest):
    """
    This endpoint is used by the Q&A bot
    """
    response = q_and_a_engine.query(request.query)
    return QAQueryResponse(response=response.message.content)

def fix_base64_padding(data: str) -> str:
    # Add padding if necessary
    return data + "=" * ((4 - len(data) % 4) % 4)

@app.post("/mm-q-and-a")
async def mm_q_and_a(req_data: MutliModalRequest):
    """
    This function is used for asking questions about images in the UI (multi-modal RAG)
    """
    try:
        # Fix padding if needed
        base64_image = fix_base64_padding(req_data.image.split(",")[1])  # Ensure you only decode the base64 part

        # Decode the base64 image
        image_data = base64.b64decode(base64_image)

        # Use PIL to open the image
        image = Image.open(BytesIO(image_data))

        # Optionally, perform any manipulation on the image if needed
        # Example: Resize the image (if required)
        # image = image.resize((512, 512))

        # Save the image into a BytesIO object to send it as a file
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)  # Move the cursor to the beginning of the buffer

        # Prepare the data for the qwen2-vl API call
        files = {
            "image": ("image.png", buffered, "image/png")
        }
        data = {
            "prompt": req_data.prompt
        }

        # Make the API call to qwen2-vl
        qwen2_vl_url = "http://192.168.5.173:8000/inference"
        response = requests.post(qwen2_vl_url, files=files, data=data)  # Sending as multipart/form-data

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            return JSONResponse(content={"response": result["response"]})
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from qwen2-vl service")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
