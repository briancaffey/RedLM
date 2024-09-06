import json
import os
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document, VectorStoreIndex
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai_like import OpenAILike

app = FastAPI()

# Global variables
index = None
query_engine = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.on_event("startup")
async def startup_event():
    global index, query_engine

    # Set up environment variables
    os.environ["OPENAI_API_KEY"] = "None"
    os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"

    # Initialize the model
    model = OpenAILike(
        model="01-ai/Yi-1.5-9B-Chat",
        api_base="http://localhost:8000/v1",
        api_key="None"
    )

    # Configure Settings
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-zh-v1.5"
    )
    Settings.llm = model

    # TODO: persist VectorStoreIndex and load from disk instead of loading on each app restart
    documents = []
    for i in range(1, 121):
        # Load and process documents
        with open(f"data/book/{i}.json", "r") as f:
            data = json.load(f)
            paragraphs = data["paragraphs"]

        for i, p in enumerate(paragraphs):
            document = Document(
                text=p["original"],
                metadata={
                    "chapter": "1",
                    "paragraph": str(i)
                },
                metadata_seperator="::",
                metadata_template="{key}=>{value}",
                text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
            )
            documents.append(document)

    # Create the index and query engine
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

@app.post("/query", response_model=QueryResponse)
async def perform_query(request: QueryRequest):
    if query_engine is None:
        raise HTTPException(status_code=500, detail="Server is not ready. Please wait for initialization.")

    response = query_engine.query(request.query)
    return QueryResponse(response=str(response))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)