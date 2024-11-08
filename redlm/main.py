import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
from pydantic import BaseModel


from .utils.rag import (
    get_qa_query_engine,
    get_q_and_a_query_engine,
    get_query_engine_for_multi_modal,
)

from .utils.misc import process_mm_qa_request, configure_observability
from .workflows.rag import RAGWorkflow

logger = logging.getLogger("uvicorn.info")

configure_observability()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str


class DocumentMetadata(BaseModel):
    chapter: int
    paragraph: int
    content: str


class QAQueryResponse(BaseModel):
    response: str
    metadata: Optional[List[DocumentMetadata]] = None
    image_desc: Optional[str] = None


class MultiModalRequest(BaseModel):
    prompt: str
    image: str
    chapter: int


@app.on_event("startup")
async def startup_event():
    global query_engine, q_and_a_engine, index
    query_engine = get_qa_query_engine()
    q_and_a_engine, index = get_q_and_a_query_engine()


@app.post("/query", response_model=QueryResponse)
async def perform_query(request: QueryRequest):
    """
    This endpoint is used by the evaluation script
    """

    response = query_engine.query(request.query)
    return QueryResponse(response=str(response))


@app.post("/q-and-a", response_model=QAQueryResponse)
async def perform_q_and_a_workflow(request: QueryRequest):
    """
    This endpoint uses a LlamaIndex Workflow to process a RAG Query
    """
    logger.info(f"💬Request for Q&A chatbot: {request}")
    w = RAGWorkflow(timeout=None)
    result = await w.run(query=request.query)

    print("Response...")
    print(result["response"].message.content)
    response = result["response"].message.content
    metadata = result["metadata"]
    return QAQueryResponse(response=response, metadata=metadata)


@app.post("/q-and-a-old", response_model=QAQueryResponse)
async def perform_q_and_a(request: QueryRequest):
    """
    This function has been deprecated in favor of using perform_q_and_a_workflow using LlamaIndex Workflows

    This endpoint is used by the Q&A bot
    """
    response = q_and_a_engine.query(request.query)
    return QAQueryResponse(response=response[0].message.content, metadata=response[1])


@app.post("/mm-q-and-a")
async def mm_q_and_a_workflow(req_data: MultiModalRequest):
    """
    This function handles Multimodal Q&A bot requests using a LlamaIndex workflow
    """
    try:
        # parse data from request object
        image_b64 = req_data.image
        prompt = req_data.prompt
        chapter = req_data.chapter

        # setup LlamaIndex Workflow and run it with data from request
        w = RAGWorkflow(timeout=None)
        result = await w.run(query=prompt, image_data=image_b64, chapter_number=chapter)

        # return response
        return QAQueryResponse(
            response=result["response"].message.content,
            metadata=result["metadata"],
            image_desc=result["image_description"],
        )
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mm-q-and-a-old")
async def mm_q_and_a_v2(req_data: MultiModalRequest):
    """
    This function has been deprecated in favor of mm_q_and_a_workflow using LlamaIndex workflows

    This function does the following
    - passes image and prompt data to the process_mm_qa_request function for image description
    - uses this data to make a query using the multi-modal QA Query engine
    - returns the results of the multi-modal QA query engine
    - Depending on configuration, either `meta/llama-3.2-90b-vision-instruct` or `Qwen2-VL-2B` (local service) is used to process image data
    """
    try:
        # response is the text description of the image in Chinese
        # uses Qwen2-VL locally OR meta/llama-3.2-90b-vision-instruct from NVIDIA API catalog
        image_b64 = req_data.image
        prompt = req_data.prompt
        image_description = process_mm_qa_request(prompt, image_b64)
        print(f"Image description: {image_description}")

        # use query engine to make query about image
        # TODO: implement this
        filters = MetadataFilters(
            filters=[ExactMatchFilter(key="chapter", value=str(req_data.chapter))]
        )

        # get the query engine with the filters
        # here we filter for the different
        query_engine = get_query_engine_for_multi_modal(filters)

        response = query_engine.custom_query(
            image_description=image_description, user_question=req_data.prompt
        )

        return QAQueryResponse(
            response=response[0].message.content,
            metadata=response[1],
            image_desc=image_description,
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
