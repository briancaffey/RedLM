import json
import os

from dotenv import load_dotenv
load_dotenv()

from llama_index.core import (
    get_response_synthesizer,
    PromptTemplate,
    Settings,
)
from llama_index.core.llms import ChatMessage
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.llms.nvidia import NVIDIA
from llama_index.llms.openai_like import OpenAILike
from .utils import get_llm, get_index

# LLMs

# Completion Model - used primarily for evaluation, defaults to 01-ai/Yi-1.5-9B
COMPLETION_MODEL = os.environ.get("COMPLETION_MODEL", "01-ai/Yi-1.5-9B")
completion_model = get_llm(model_name=COMPLETION_MODEL)

# Chat Model - used for Q&A bot and Multi-Modal Q&A Bot
# defaults to baichuan-inc/baichuan2-13b-chat or 01-ai/Yi-1.5-9B-Instruct
# depending on NVIDIA_API_KEY
model = get_llm()
index = get_index()


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

mm_q_and_a_prompt = PromptTemplate(
    "这是书中相关的内容：\n"
    "{context_str}\n"
    "---------------------\n"
    "下面是场景的描述：\n"
    "---------------------\n"
    "{query_str}\n"
    "---------------------\n"
    "根据上述的信息，尽量解释上说的场景和书的关系。"
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
        metadata = []
        # Collect the metadata into a list of dicts so that it can be sent to UI for references
        for node in nodes:
            metadata_dict = {}
            node_metadata = node.node.metadata
            metadata_dict["content"] = node.node.text
            metadata_dict["chapter"] = int(node_metadata.get("chapter"))
            metadata_dict["paragraph"] = int(node_metadata.get("paragraph"))

            metadata.append(metadata_dict)

        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        response = self.llm.chat(
            [
                ChatMessage(
                    role="user",
                    content=q_and_a_prompt.format(
                        context_str=context_str, query_str=query_str
                    ),
                )
            ]
        )

        return response, metadata


def get_qa_query_engine():
    """
    Query engine used for evaluation with RAG (uses completion)
    """

    # Configure Settings
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
    Settings.llm = model

    retriever = index.as_retriever()

    synthesizer = get_response_synthesizer(response_mode="compact")

    query_engine = QAQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        llm=completion_model,
        qa_prompt=qa_prompt,
    )

    return query_engine


def get_q_and_a_query_engine():
    """
    Query engine to be used for asking questions (uses chat format)
    """

    # Configure Settings
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
    Settings.llm = model

    retriever = index.as_retriever()

    synthesizer = get_response_synthesizer(response_mode="compact")

    query_engine = QAndAQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        llm=model,
        qa_prompt=q_and_a_prompt,
    )

    return query_engine, index


def get_query_engine_for_multi_modal(index, filters):
    """
    This function returns the query engine used for mutli-modal Q&A
    The index is the index from the global scope in main.py
    Filters are determined in the query parameters for the route that uses this engine
    """
    retriever = index.as_retriever(filters=filters)
    synthesizer = get_response_synthesizer(response_mode="compact")
    try:
        query_engine = QAndAQueryEngine(
            retriever=retriever,
            response_synthesizer=synthesizer,
            llm=model, # TOOD: set max_tokens=1024 when using completion
            qa_prompt=mm_q_and_a_prompt,
        )
    except Exception as e:
        print(e)
    return query_engine
