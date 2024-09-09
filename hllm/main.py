from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    print(dir(response))
    print(response)
    return QAQueryResponse(response=response.message.content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
