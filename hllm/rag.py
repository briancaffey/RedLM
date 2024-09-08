import json

from llama_index.core import (
    Document,
    get_response_synthesizer,
    load_index_from_storage,
    PromptTemplate,
    Settings,
    StorageContext,
)
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


def get_qa_query_engine():

    # Initialize the model
    model = OpenAILike(
        model="01-ai/Yi-1.5-9B-Chat",
        api_base="http://localhost:8000/v1",
        api_key="None",
    )

    # Configure Settings
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
    Settings.llm = model

    # TODO: persist VectorStoreIndex and load from disk instead of loading on each app restart

    # documents = []
    # for chapter in range(1, 121):
    #     # Load and process documents
    #     with open(f"data/book/{chapter}.json", "r") as f:
    #         data = json.load(f)
    #         paragraphs = data["paragraphs"]

    #     for i, p in enumerate(paragraphs):
    #         document = Document(
    #             text=p["original"],
    #             metadata={"chapter": str(chapter), "paragraph": str(i)},
    #             metadata_seperator="::",
    #             metadata_template="{key}=>{value}",
    #             text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
    #         )
    #         documents.append(document)

    # # Create the index and query engine
    # # index = VectorStoreIndex.from_documents(documents)
    # index = VectorStoreIndex.from_documents(documents)

    # # store
    # index.storage_context.persist(persist_dir="storage")

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
