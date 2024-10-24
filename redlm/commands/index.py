"""
Command used to build the Vector Store Index

Usage:

python -m commands.index
"""

import json

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


en_embedding_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
zh_embedding_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
# Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")


def persist_index():
    documents = []
    for chapter in range(1, 121):
        # Load and process documents
        with open(f"data/book/{chapter}.json", "r") as f:
            data = json.load(f)
            paragraphs = data["paragraphs"]

        for i, p in enumerate(paragraphs):
            for lang in ["original", "chinese", "english"]:
                document = Document(
                    text=p[lang],
                    metadata={
                        "chapter": str(chapter),
                        "paragraph": str(i),
                        "language": lang,
                    },
                    metadata_seperator="::",
                    metadata_template="{key}=>{value}",
                    text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
                    embed_model=(
                        en_embedding_model if lang == "english" else zh_embedding_model
                    ),
                )
                documents.append(document)

    # Create the index and query engine
    # index = VectorStoreIndex.from_documents(documents)
    index = VectorStoreIndex.from_documents(documents)

    # store context in storage directory
    # TODO: check to see if there are any JSON files in the storage directory
    # Build and persist the VectorStoreIndex
    # for now, run `python -m commands.index` before running the server
    index.storage_context.persist(persist_dir="storage")


if __name__ == "__main__":
    persist_index()
