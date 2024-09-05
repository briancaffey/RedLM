"""
This script shows how to build a basic RAG query engine using custom documents
"""

import json
import os

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document, VectorStoreIndex
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai_like import OpenAILike

os.environ["OPENAI_API_KEY"] = "None"
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"
model = OpenAILike(
    model="01-ai/Yi-1.5-9B-Chat",
    api_base="http://localhost:8000/v1",
    api_key="None"
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-zh-v1.5"
)

Settings.llm = model

with open("data/book/1.json", "r") as f:
    data = f.read()
    data = json.loads(data)
    paragraphs = data["paragraphs"]


documents = []
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

    # print(
    #     "The LLM sees this: \n",
    #     document.get_content(metadata_mode=MetadataMode.LLM),
    # )
    # print(
    #     "The Embedding model sees this: \n",
    #     document.get_content(metadata_mode=MetadataMode.EMBED),
    # )

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

# answer is 《好了歌》
QUERY = "士隐的歌叫什么？"

#
print("With Context")
print("======")
response = query_engine.query(QUERY)
print(response)

print()
print("Without using Context")
print("======")
response = model.chat([ChatMessage(role="user", content=QUERY)])
print(response)