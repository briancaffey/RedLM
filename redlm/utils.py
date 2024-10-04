import os
import requests, base64
import base64
from io import BytesIO
from PIL import Image


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
    - LLM_NAME is the main chat LLM model to use
    - setting NVIDIA_API_KEY will use NVIDIA cloud APIs for LLM inference
    - LLM_SERVICE_HOST and LLM_SERVICE_PORT can be configured to use local LLMs
    """

    MODEL_NAME = model_name or os.environ.get(
        "LLM_NAME", "baichuan-inc/baichuan2-13b-chat"
    )

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
        print("Using NVIDIA Cloud API for inference")

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
    - define logic for 2 major logical flows: qwen2-vl and llama-3.2-90b-vision-instruct
    """

    image_b64 = req_data.image
    # TODO: should the prompt (user input from image Q&A form) be used below in the user message?
    prompt = req_data.prompt

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
                    "content": f'这张图片是一幅中国古典绘画的一部分。请描述这张图片的内容： <img src="data:image/png;base64,{image_b64}" />',
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
