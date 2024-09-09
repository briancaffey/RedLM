import json

from llama_index.core import (
    get_response_synthesizer,
    load_index_from_storage,
    PromptTemplate,
    Settings,
    StorageContext,
)
from llama_index.core.llms import ChatMessage
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.llms.openai_like import OpenAILike


qa_prompt = PromptTemplate(
    "这是相关的参考资料：\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "根据上述的参考资料，回答下面的问题\n"
    "问题：{query_str}\n"
    "答案：\n"
)

q_and_a_prompt = PromptTemplate(
    "这是相关的参考资料：\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "根据上述的参考资料，回答下面的问题\n"
    "问题：{query_str}\n"
)


class QAQueryEngine(CustomQueryEngine):
    """RAG Completion Query Engine optimized for Q&A"""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAILike
    qa_prompt: PromptTemplate

    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)
        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        response = self.llm.complete(
            qa_prompt.format(context_str=context_str, query_str=query_str)
        )

        return str(response)

class QAndAQueryEngine(CustomQueryEngine):
    """RAG Completion Query Engine optimized for Q&A"""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAILike
    qa_prompt: PromptTemplate

    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)
        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        response = self.llm.chat(
            [ChatMessage(role="user", content=q_and_a_prompt.format(context_str=context_str, query_str=query_str))]
        )

        return response


def get_qa_query_engine():

    # Initialize the model
    model = OpenAILike(
        model="01-ai/Yi-1.5-9B-Chat",
        api_base="http://localhost:8000/v1",
        api_key="None",
        # keep this number small since we don't need a long explination for multiple-choice test evaluation
        max_tokens=16
    )

    # Configure Settings
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
    Settings.llm = model

    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(storage_context)

    retriever = index.as_retriever()

    synthesizer = get_response_synthesizer(response_mode="compact")

    query_engine = QAQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        llm=model,
        qa_prompt=qa_prompt,
    )

    return query_engine

def get_q_and_a_query_engine():
    """
    Query engine to be used for asking questions (uses chat format)
    """
    # Initialize the model
    model = OpenAILike(
        model="01-ai/Yi-1.5-9B-Chat",
        api_base="http://localhost:8000/v1",
        api_key="None",
        max_tokens=1024
    )

    # Configure Settings
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
    Settings.llm = model

    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(storage_context)

    retriever = index.as_retriever()

    synthesizer = get_response_synthesizer(response_mode="compact")

    query_engine = QAndAQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        llm=model,
        qa_prompt=q_and_a_prompt,
    )

    return query_engine