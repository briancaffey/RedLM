import os
import requests, base64
import base64
import logging
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image

logger = logging.getLogger("uvicorn.info")
load_dotenv()


from llama_index.llms.nvidia import NVIDIA
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import (
    load_index_from_storage,
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.milvus import MilvusVectorStore

from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler


def get_llm(model_name=None, is_completion_model=None):
    """
    Helper function for setting the LLM to use for inference
    - LLM options are configured via environment variables
    - LLM_NAME is the main chat LLM model to use
    - setting NVIDIA_API_KEY will use NVIDIA cloud APIs for LLM inference
    - LLM_SERVICE_HOST and LLM_SERVICE_PORT can be configured to use local LLMs
    """

    MODEL_NAME = model_name or os.environ.get(
        "LLM_NAME", "baichuan-inc/baichuan2-13b-chat"
    )

    if is_completion_model:
        logger.info("Completion Model Info:")
    else:
        logger.info("Chat Model Info:")

    # use NVIDIA API catalog if NVIDIA_API_KEY is set and valid
    if os.environ.get("NVIDIA_API_KEY"):
        assert os.environ.get("NVIDIA_API_KEY").startswith(
            "nvapi-"
        ), "Invalid NVIDIA API key"
        api_key = os.environ.get("NVIDIA_API_KEY")

        # NVIDIA API catalog model, defaults to Baichuan2-13B-Chat
        # Other options:
        #   01-ai/yi-large
        #   qwen/qwen2-7b-instruct
        model = NVIDIA(model=MODEL_NAME)
        logger.info("🟩Using NVIDIA Cloud API for inference")

    # otherwise, use a generic OpenAI API compatible service, e.g. vLLM
    else:
        LLM_SERVICE_HOST = os.environ.get("LLM_SERVICE_HOST", "localhost")
        LLM_SERVICE_PORT = os.environ.get("LLM_SERVICE_PORT", "8000")
        model = OpenAILike(
            model=MODEL_NAME,
            api_base=f"http://{LLM_SERVICE_HOST}:{LLM_SERVICE_PORT}/v1",
            api_key="None",
            max_tokens=1024,
        )
        logger.info("🖥️Using local model for inference")

    if is_completion_model:
        logger.info(f"Completion Model: {MODEL_NAME}")
    else:
        logger.info(f"Chat Model: {MODEL_NAME}")

    return model


def get_index():
    """
    Gets the index either from a remote Milvus server or from in-memory VectorIndexStore
    Returns the index and a boolean value: True if the index is a Milvus server, otherwise False
    This utility function is used when defining query engines in rag.py and the script useed for indexing
    """
    VECTORDB_SERVICE_HOST = os.environ.get(
        "VECTORDB_SERVICE_HOST", "localhost"
    )  # localhost
    VECTORDB_SERVICE_PORT = os.environ.get("VECTORDB_SERVICE_PORT", "19530")  # 19530
    USE_EXTERNAL_VECTORDB = os.environ.get("USE_EXTERNAL_VECTORDB", False)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")

    VECTORDB_URI = None
    if VECTORDB_SERVICE_HOST and VECTORDB_SERVICE_PORT:
        VECTORDB_URI = f"http://{VECTORDB_SERVICE_HOST}:{VECTORDB_SERVICE_PORT}"

    if VECTORDB_URI and USE_EXTERNAL_VECTORDB:
        logger.info("🦅Using Milvus vector database...")
        vector_store = MilvusVectorStore(
            # BAAI/bge-small-{en,zh}-v1.5 has Dimension of 384, Sequence Length of 512
            # https://huggingface.co/BAAI/bge-small-zh-v1.5#evaluation
            uri=VECTORDB_URI,
            dim=512,
            overwrite=False,
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context
        )
    else:
        print("Loading index from storage directory...")
        storage_context = StorageContext.from_defaults(persist_dir="storage")
        index = load_index_from_storage(storage_context)
        print("Finished loading index.")

    return index, bool(USE_EXTERNAL_VECTORDB)


def resize_image_b64(image_b64):
    """
    Images sent to NVIDIA API must be under 180,000 bytes
    This function resizes images to fit under the image size limit
    """

    # Decode the base64 image
    image_data = base64.b64decode(image_b64)

    # Open the image with Pillow
    image = Image.open(BytesIO(image_data))

    # Maximum size in bytes
    max_size_in_bytes = 180_000

    # Save the original image into a buffer to get its size
    buffer = BytesIO()
    image.save(buffer, format="PNG", quality=85)
    original_size_in_bytes = buffer.tell()

    # If the image is already smaller than 180,000 bytes, return as is
    if original_size_in_bytes <= max_size_in_bytes:
        return image_b64

    # Calculate the scaling factor to resize the image based on the size ratio
    scale_factor = (max_size_in_bytes / original_size_in_bytes) ** 0.5

    # Calculate the new size for the image
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Save the resized image in memory
    buffer = BytesIO()
    resized_image.save(buffer, format="PNG", quality=85)

    # Encode the resized image to base64
    resized_image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return resized_image_b64


def fix_base64_padding(data: str) -> str:
    # Add padding if necessary
    return data + "=" * ((4 - len(data) % 4) % 4)


def process_mm_qa_request(req_data):
    """
    This function process requests for the multi-modal Q&A bot

    - req_data contains the prompt question and the base64 image data
    - this info is used to get a description of the image (in Chinese or English)
    - define logic for 2 major logical flows: inference with qwen2-vl and llama-3.2-90b-vision-instruct
    """

    image_b64 = req_data.image
    prompt = req_data.prompt

    cn_prompt = "这张图片是一幅中国古典绘画的一部分。"
    en_prompt = "This is an image of a classical Chinese painting. "

    image_description_prompt = cn_prompt if is_chinese_text(prompt) else en_prompt

    image_b64 = fix_base64_padding(image_b64.split(",")[1])

    # use NVIDIA APIs for image processing
    if os.environ.get("NVIDIA_API_KEY"):
        assert os.environ.get("NVIDIA_API_KEY").startswith(
            "nvapi-"
        ), "Invalid NVIDIA API key"
        api_key = os.environ.get("NVIDIA_API_KEY")

        # fuyu-8b was used initially, but llama-3.2-90b-vision-instruct has the same API format
        # llama-3.2 also has better support for Chinese compared to fuyu-8b
        default_invoke_url = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions"
        invoke_url = os.environ.get("VLM_INVOKE_URL", default_invoke_url)
        stream = False

        if len(image_b64) >= 180_000:
            image_b64 = resize_image_b64(image_b64)

        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

        default_vlm_model_name = "meta/llama-3.2-90b-vision-instruct"
        vlm_model_name = os.environ.get("VLM_MODEL_NAME", default_vlm_model_name)

        payload = {
            "model": vlm_model_name,
            "messages": [
                {
                    "role": "user",
                    # This image is part of a classical Chinese painting. Please describe the content of this image:
                    "content": f'{image_description_prompt}\n{prompt} <img src="data:image/png;base64,{image_b64}" />',
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.20,
            "top_p": 0.70,
            "seed": 0,
            "stream": stream,
        }

        response = requests.post(invoke_url, headers=headers, json=payload)

        if stream:
            for line in response.iter_lines():
                if line:
                    print(line.decode("utf-8"))
        else:
            # print(response.json())

            ret = response.json()["choices"][0]["message"]["content"]

            print(ret)
            return ret

    # use local model (qwen2-vl) with locally running service
    # see services/qwen2-vl directory for service details
    else:
        # Decode the base64 image
        image_data = base64.b64decode(image_b64)

        # Use PIL to open the image
        image = Image.open(BytesIO(image_data))

        # Optionally, perform any manipulation on the image if needed
        # Example: Resize the image (if required)
        # image = image.resize((512, 512))

        # Save the image into a BytesIO object to send it as a file
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)  # Move the cursor to the beginning of the buffer

        # Prepare the data for the qwen2-vl API call
        files = {"image": ("image.png", buffered, "image/png")}
        data = {"prompt": req_data.prompt}

        # Make the API call to the local qwen2-vl service (Vision Language Model Service)
        VLM_SERVICE_HOST = os.environ.get("VLM_SERVICE_HOST", "192.168.5.173")
        VLM_SERVICE_PORT = os.environ.get("VLM_SERVICE_PORT", "8000")
        qwen2_vl_url = f"http://{VLM_SERVICE_HOST}:{VLM_SERVICE_PORT}/inference"

        vision_model_response = requests.post(
            qwen2_vl_url, files=files, data=data
        )  # Sending as multipart/form-data

        return vision_model_response.json()["response"]


def is_chinese_text(text: str) -> bool:
    """
    This is a simple helper function that is used to determine which prompt to use
    depending on the language of the original user query
    """
    chinese_count = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    english_count = sum(1 for char in text if "a" <= char.lower() <= "z")

    return chinese_count > english_count


def configure_observability():
    """
    Configure Observability and Tracing
    """

    LANGFUSE_SERVICE_HOST = os.environ.get("LANGFUSE_SERVICE_HOST", "localhost")
    LANGFUSE_SERVICE_PORT = os.environ.get("LANGFUSE_SERVICE_PORT", "3030")
    LANGFUSE_DOMAIN = f"http://{LANGFUSE_SERVICE_HOST}:{LANGFUSE_SERVICE_PORT}"
    LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", None)
    LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", None)
    os.environ["LANGFUSE_HOST"] = LANGFUSE_DOMAIN

    USE_LANGFUSE = LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY

    if USE_LANGFUSE:
        logger.info("🪢 Using Langfuse for Tracing and Observability ")
        langfuse_callback_handler = LlamaIndexCallbackHandler(
            public_key=LANGFUSE_PUBLIC_KEY,
            secret_key=LANGFUSE_SECRET_KEY,
            host=LANGFUSE_DOMAIN,
        )

        # Settings = CallbackManager([langfuse_callback_handler])

        langfuse_callback = CallbackManager([langfuse_callback_handler])
        return langfuse_callback
