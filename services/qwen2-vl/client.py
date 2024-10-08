"""
This script is used to test the Qwen2-VL service

Usage: python client.py --host 192.168.1.123 --port 8001

It should return a description of test.png which is a picture of a cat
"""

import argparse

import requests

parser = argparse.ArgumentParser(description="Client script")
parser.add_argument("--host", type=str, default="localhost", help="Host address")
parser.add_argument("--port", type=int, default=8000, help="Port number")
args = parser.parse_args()

host = args.host
port = args.port

# API endpoint URL
url = f"http://{host}:{port}/inference"

# Path to the local image file
image_path = "test.png"

# Text prompt
prompt = "Please describe what is in this image"

# Prepare the files and data for the POST request
files = {
    "image": ("test.png", open(image_path, "rb"), "image/png")
}
data = {
    "prompt": prompt
}

try:
    # Send POST request to the API
    response = requests.post(url, files=files, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        print("API Response:")
        print(result["response"])
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

finally:
    # Close the file
    files["image"][1].close()