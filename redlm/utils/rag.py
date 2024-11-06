import json
import logging
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
from llama_index.core.schema import NodeWithScore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.llms.nvidia import NVIDIA
from llama_index.llms.openai_like import OpenAILike

from .misc import get_llm, get_index, is_chinese_text, configure_observability

langfuse_callback = configure_observability()
logger = logging.getLogger('uvicorn.info')

# LLMs
# Completion Model - used primarily for evaluation, defaults to 01-ai/Yi-1.5-9B
COMPLETION_MODEL = os.environ.get("COMPLETION_MODEL", "01-ai/Yi-1.5-9B")
completion_model = get_llm(model_name=COMPLETION_MODEL, is_completion_model=True)

# Chat Model - used for Q&A bot and Multi-Modal Q&A Bot
# defaults to baichuan-inc/baichuan2-13b-chat or 01-ai/Yi-1.5-9B-Instruct
# depending on NVIDIA_API_KEY
model = get_llm()
index, _ = get_index()


# this prompt is used for evaluations
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
    "问题：{user_question}\n"
)

q_and_a_prompt_english = PromptTemplate(
    "This is some related reference material:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Based on the above material, answer the following question:\n"
    "Question: {user_question}\n"
)

mm_q_and_a_prompt = PromptTemplate(
    "这是书中相关的内容：\n"
    "{context_str}\n"
    "---------------------\n"
    "下面是场景的描述：\n"
    "---------------------\n"
    "{image_description}\n"
    "---------------------\n"
    "根据上述的信息，尽量解释上说的场景和书的关系。"
)

mm_q_and_a_prompt_english = PromptTemplate(
    "Here is relevant content from the book:\n"
    "{context_str}\n"
    "---------------------\n"
    "Below is the description of a scene:\n"
    "---------------------\n"
    "{image_description}\n"
    "---------------------\n"
    "Based on the information provided above, try to explain the relationship between the described scene and the book content."
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
    """
    RAG Completion Query Engine optimized for Q&A

    - this class handles both text-based Q&A bot queries and image-based Q&A bot queries
    - this class can optionally be used with LlamaIndex workflows, in which case nodes_from_workflow will be used
    """

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAILike
    # qa_prompt: PromptTemplate

    def custom_query(
            self, user_question: str = None,
            image_description: str = None,
            nodes_from_workflow: list[NodeWithScore] = None,
        ):
        """
        user_question is the original query entered byt the user in the UI
        image_description is the description of the image returned by the VLM service
        """
        logger.info("Handling custom query...")
        # if image_description is present, we are processing a multi-modal request (a query about an image)
        if image_description:
            logger.info("🖼️Image-based Q&A query")
            if is_chinese_text(user_question):
                logger.info("🇨🇳Text is Chinese")
                prompt = mm_q_and_a_prompt
            else:
                logger.info("🇬🇧Text is English")
                prompt = mm_q_and_a_prompt_english
        else:
            logger.info("💬Text-based Q&A query")
            if is_chinese_text(user_question):
                logger.info("🇨🇳Text is Chinese")
                prompt = q_and_a_prompt
            else:
                logger.info("🇬🇧Text is English")
                prompt = q_and_a_prompt_english

        # if nodes_from_workflow are passed in, then we can use the ranked nodes from the RerankEvent
        # otherwise we do the RAG retrieval here directly in the QAndAQueryEngine
        if nodes_from_workflow:
            logger.info("Using nodes from workflow...")
            nodes = nodes_from_workflow
        else:
            logger.info("Querying nodes in CustomQueryEngine...")
            # do retrieval with RAG system
            # if we are doing a text-based Q&A query, we only need to use the user query
            if not image_description:
                nodes = self.retriever.retrieve(user_question)
            else:
                # here we want to try finding passages that closely align with the description of the image
                # the original user query was already used in getting the image description, and it will be used again in the final query
                nodes = self.retriever.retrieve(image_description)

        metadata = []
        # Collect the metadata into a list of dicts so that it can be sent to UI for references
        for node in nodes:
            metadata_dict = {}
            node_metadata = node.node.metadata
            metadata_dict["content"] = node.node.text
            metadata_dict["chapter"] = int(node_metadata.get("chapter"))
            metadata_dict["paragraph"] = int(node_metadata.get("paragraph"))

            metadata.append(metadata_dict)

        # format the paragraphs from the RAG response into a string
        context_str = "\n\n".join([n.node.get_content() for n in nodes])

        # format the final query that will be used to respond to the query
        if image_description:
            logger.info("Formatting prompt for multi-modal request")
            content = prompt.format(context_str=context_str, image_description=image_description)
            logger.info(f"Prompt is \n\n{content}")
        else:
            logger.info("Formatting prompt")
            content = prompt.format(context_str=context_str, user_question=user_question)
            logger.info(f"Prompt is \n\n{content}")

        response = self.llm.chat(
            [
                ChatMessage(
                    role="user",
                    content=content,
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
    Settings.callback_manager = langfuse_callback
    Settings.llm = model

    retriever = index.as_retriever(similarity_top_k=2)
    synthesizer = get_response_synthesizer(response_mode="compact")

    query_engine = QAndAQueryEngine(
        retriever=retriever,
        response_synthesizer=synthesizer,
        llm=model,
        # qa_prompt=q_and_a_prompt,
        # https://github.com/run-llama/llama_index/discussions/14251#discussioncomment-9822722
        callback_manager=langfuse_callback,
    )

    return query_engine, index


def get_query_engine_for_multi_modal(filters):
    """
    This function returns the query engine used for multi-modal Q&A
    The index is the index from the global scope in main.py
    Filters are determined in the query parameters for the route that uses this engine
    """
    Settings.callback_manager = langfuse_callback
    retriever = index.as_retriever(filters=filters, similarity_top_k=2)
    synthesizer = get_response_synthesizer(response_mode="compact")
    try:
        query_engine = QAndAQueryEngine(
            retriever=retriever,
            response_synthesizer=synthesizer,
            llm=model,
            # qa_prompt=mm_q_and_a_prompt,
            callback_manager=langfuse_callback,
        )
    except Exception as e:
        print(e)
    return query_engine
