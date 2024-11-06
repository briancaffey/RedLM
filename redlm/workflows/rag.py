import re

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

from utils.misc import get_llm, get_index

from utils.rag import (
    # get_qa_query_engine,
    get_q_and_a_query_engine,
    # get_query_engine_for_multi_modal,
)


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
    This is a LlamaIndex Workflow that demonstrates how to do RAG with
    """

    @step
    async def retrieve(self, ctx: Context, ev: StartEvent) -> RetrieverEvent | None:
        """
        Entry point for RAG, triggered by a StartEvent with `query`.

        """
        query = ev.get("query")

        if not query:
            return None

        print(f"Query the database with: {query}")

        # store the query in the global context
        await ctx.set("query", query)

        index, _ = get_index()

        # get the index from the global context
        if index is None:
            print("Index is empty, load some documents before querying!")
            return None

        retriever = index.as_retriever(similarity_top_k=4)
        nodes = await retriever.aretrieve(query)
        print(f"Retrieved {len(nodes)} nodes.")
        return RetrieverEvent(nodes=nodes)

    @step
    async def rerank(self, ctx: Context, ev: RetrieverEvent) -> RerankEvent:
        print("🔀Doing reranking")
        # Rerank the nodes
        ranker = LLMRerank(
            choice_batch_size=2,
            top_n=2,
            llm=get_llm(),
            parse_choice_select_answer_fn=custom_parse_choice_select_answer_fn,
        )
        print(await ctx.get("query", default=None), flush=True)
        new_nodes = ranker.postprocess_nodes(
            ev.nodes, query_str=await ctx.get("query", default=None)
        )
        print(f"Reranked nodes to {len(new_nodes)}")
        return RerankEvent(nodes=new_nodes)

    @step
    async def inference(self, ctx: Context, ev: RerankEvent) -> StopEvent:
        """
        Do LLM inference using original query and selected nodes from RerankEvent
        """
        print("🔀Doing inference step")
        query = await ctx.get("query", default=None)
        print("Getting query engine..")
        qa_query_engine, _ = get_q_and_a_query_engine()
        print("Getting response from custom query engine")
        response = qa_query_engine.custom_query(
            user_question=query, nodes_from_workflow=ev.nodes
        )
        return StopEvent(result=response)


# uncomment the following to generate workflow visualization
# draw_all_possible_flows(RAGWorkflow, filename="workflows/viz/rag_workflow.html")

# test the workflow by uncommenting the code below and running the following command:
# python -m workflows.rag

# async def main():
#     w = RAGWorkflow()
#     result = await w.run(query="贾宝玉的父亲对他有什么看法？")
#     print(result)


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())
