from fastapi import FastAPI
from pydantic import BaseModel

from .rag import get_qa_query_engine


app = FastAPI()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str


@app.on_event("startup")
async def startup_event():
    global query_engine
    query_engine = get_qa_query_engine()


@app.post("/query", response_model=QueryResponse)
async def perform_query(request: QueryRequest):
    """
    This endpoint is used by the evaluation script
    """

    response = query_engine.query(request.query)
    return QueryResponse(response=str(response))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
