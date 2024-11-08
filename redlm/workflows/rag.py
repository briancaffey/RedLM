import re
import logging

from llama_index.utils.workflow import draw_all_possible_flows

from llama_index.core.postprocessor.llm_rerank import LLMRerank
from llama_index.core.indices.utils import default_parse_choice_select_answer_fn
from llama_index.core.workflow import (
    Context,
    Workflow,
    StartEvent,
    StopEvent,
    step,
)

from llama_index.core import Settings

from llama_index.core.workflow import Event
from llama_index.core.schema import NodeWithScore

from redlm.utils.misc import get_llm, get_index, process_mm_qa_request

from redlm.utils.rag import (
    # get_qa_query_engine,
    get_q_and_a_query_engine,
    # get_query_engine_for_multi_modal,
)

logger = logging.getLogger("uvicorn.info")


class QueryEvent(Event):
    """
    Simple Text query using RAG
    """

    query: str


class ImageAnalysisEvent(Event):
    """
    Result of using a vision language model to analyze an image
    """

    image_data: str
    chapter_number: str
    query: str


class RetrieverEvent(Event):
    """Result of running retrieval"""

    nodes: list[NodeWithScore]


class RerankEvent(Event):
    """Result of running reranking on retrieved nodes"""

    nodes: list[NodeWithScore]


# https://github.com/run-llama/llama_index/issues/3258
# https://github.com/run-llama/llama_index/issues/11470#issuecomment-2456302654
def custom_parse_choice_select_answer_fn(answer: str, num_choices: int):
    matches = re.findall(r"(Doc: \d+, Relevance: \d+)", answer)
    answer = ""
    for match in matches:
        answer += match + "\n"
    _answer = answer
    return default_parse_choice_select_answer_fn(_answer, num_choices)


class RAGWorkflow(Workflow):
    """
    LlamaIndex Workflow that implements logic for text and image Q&A bots using RAG
    """

    @step
    async def route(
        self, ctx: Context, ev: StartEvent
    ) -> ImageAnalysisEvent | QueryEvent:
        # set inputs to context
        logger.info("🔀Routing Workflow to next step")

        query = ev.get("query")
        image_data = ev.get("image_data")
        chapter_number = ev.get("chapter_number")

        # use this later in the workflow when doing metadata filtering in RAG query
        await ctx.set("chapter_number", chapter_number)

        # if image_data and chapter number are provided, process the image data
        if image_data:
            logger.info("🖼️Routing to ImageAnalysisEvent")
            return ImageAnalysisEvent(
                image_data=image_data,
                chapter_number=str(chapter_number),
                query=query,
            )

        else:
            logger.info("💬Routing to QueryEvent")
            return QueryEvent(query=query)

    @step
    async def image_processing(
        self, ctx: Context, ev: ImageAnalysisEvent
    ) -> QueryEvent:
        """
        Do image processing using VLM to get image description
        """
        logger.info("🖼️ Getting image description...")
        image_description = process_mm_qa_request(ev.query, ev.image_data)
        logger.info(f"🖼️ Image description is\n\n{image_description}\n\n")
        logger.info("💿 Saving image description to context")
        await ctx.set("image_description", image_description)
        return QueryEvent(query=image_description)

    @step
    async def retrieve(self, ctx: Context, ev: QueryEvent) -> RetrieverEvent | None:
        """
        Entry point for RAG, triggered by a StartEvent with `query`.
        """
        # query = ev.get("query")
        query = ev.query
        image_description = await ctx.get("image_description", default=None)

        if image_description:
            query = image_description

        logger.info(f"🧮Query the vector database with: {query}")

        # store the query in the global context
        await ctx.set("query", query)

        index, _ = get_index()

        # get the index from the global context
        if index is None:
            logger.info("🕳️Index is empty, load some documents before querying!")
            return None

        # get the four most relevant nodes base on cosine similarity
        retriever = index.as_retriever(similarity_top_k=4)
        nodes = await retriever.aretrieve(query)
        logger.info(f"📐Retrieved {len(nodes)} nodes.")
        return RetrieverEvent(nodes=nodes)

    @step
    async def rerank(self, ctx: Context, ev: RetrieverEvent) -> RerankEvent:
        """
        Rerank nodes from a RetrieverEvent using LLMRerank
        """
        logger.info("🔀Doing LLMRerank")
        # Rerank the nodes
        ranker = LLMRerank(
            choice_batch_size=2,
            top_n=2,
            llm=get_llm(),
            parse_choice_select_answer_fn=custom_parse_choice_select_answer_fn,
        )
        query = await ctx.get("query", default=None)
        # logger.info(f"📑Rerank query is: \n\n{query}")
        new_nodes = ranker.postprocess_nodes(ev.nodes, query_str=query)
        logger.info(f"🔢Reranked nodes to {len(new_nodes)}")
        return RerankEvent(nodes=new_nodes)

    @step
    async def inference(self, ctx: Context, ev: RerankEvent) -> StopEvent:
        """
        Do LLM inference using original query and selected nodes from RerankEvent
        """
        logger.info("🤖Doing inference step")
        query = await ctx.get("query", default=None)
        logger.info("⚙️ Getting query engine..")
        qa_query_engine, _ = get_q_and_a_query_engine()
        logger.info("🔎Getting response from custom query engine")

        # get image description from context

        image_description_ctx = await ctx.get("image_description", default=None)

        # https://github.com/run-llama/llama_index/issues/15748
        # https://github.com/run-llama/llama_index/pull/16756/commits/02b9b133b5c80a17d0385814a1d49810be0217d1
        if image_description_ctx is not None:
            image_description = image_description_ctx
        else:
            image_description = None

        response, metadata = qa_query_engine.custom_query(
            user_question=query,
            image_description=image_description,
            nodes_from_workflow=ev.nodes,
        )
        # return StopEvent(response=response, metadata=metadata)
        return StopEvent(
            result={
                "response": response,
                "image_description": image_description,
                "metadata": metadata,
            }
        )
