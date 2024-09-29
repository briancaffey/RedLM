"""
Script for testing adept/fuyu-8b vision model for image comprehension

TODO: implement image resizing to keep image below 180_000
"""

import base64
import os
import requests

from dotenv import load_dotenv

load_dotenv()


invoke_url = "https://ai.api.nvidia.com/v1/vlm/adept/fuyu-8b"
stream = False

with open("scripts/test.png", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

print("Image size.....")
print(len(image_b64))
assert (
    len(image_b64) < 180_000
), "To upload larger images, use the assets API (see docs)"

API_KEY = os.environ.get("NVIDIA_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "text/event-stream" if stream else "application/json",
}

payload = {
    "messages": [
        {
            "role": "user",
            "content": f'What do you see in the following image? <img src="data:image/png;base64,{image_b64}" />',
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
    image_description = response.json()["choices"][0]["message"]["content"]
    print(image_description)
