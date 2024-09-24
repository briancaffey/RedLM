import os

from llama_index.llms.nvidia import NVIDIA
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import (
    load_index_from_storage,
    Settings,
    StorageContext,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def get_llm(model_name=None):
    """
    Helper function for setting the LLM to use for inference
    - LLM options are configured via environment variables
    """

    MODEL_NAME = model_name or os.environ.get(
        "LLM_NAME",
        "baichuan-inc/baichuan2-13b-chat"
    )

    # use NVIDIA API catalog if NVIDIA_API_KEY is set and valid
    if os.environ.get("NVIDIA_API_KEY"):
        assert os.environ.get("NVIDIA_API_KEY").startswith("nvapi-"), "Invalid NVIDIA API key"
        api_key = os.environ.get("NVIDIA_API_KEY")

        # NVIDIA API catalog model, defaults to Baichuan2-13B-Chat
        # Other options:
        #   01-ai/yi-large
        #   qwen/qwen2-7b-instruct
        model = NVIDIA(model=MODEL_NAME)
        print("Using NVIDIA Cloud API for inference")

    # otherwise, use a generic OpenAI API compatible service, e.g. vLLM
    else:
        LLM_SERVICE_HOST = os.environ.get("LLM_SERVICE_HOST", "localhost")
        LLM_SERVICE_PORT = os.environ.get("LLM_SERVICE_PORT", "8000")
        model = OpenAILike(
            model=MODEL_NAME,
            api_base=f"http://{LLM_SERVICE_HOST}:{LLM_SERVICE_PORT}/v1",
            api_key="None"
        )
        print("Using local model for inference")

    print(f"Model: {MODEL_NAME}")

    return model

def get_index():
    """
    Loads the index from disk into memory and returns the index
    - used when defining query engines
    - TODO: replace with Milvus and use either external Milvus service or Milvus Lite
    """
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
    print("Loading index...")
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(storage_context)
    print("Finished loading index.")

    return index
