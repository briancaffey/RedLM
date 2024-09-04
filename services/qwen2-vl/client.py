import requests

# API endpoint URL
url = "http://localhost:8000/inference"

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