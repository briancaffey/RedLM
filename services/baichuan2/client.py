import requests

# Define the endpoint URL
url = "http://127.0.0.1:8000/v1/chat/completions"

# Define the payload with the list of messages
payload = {
    "messages": [
        {"role": "user", "content": "Hello, how are you?"},
    ]
}

# Set the headers for the request
headers = {
    "Content-Type": "application/json"
}

# Send a POST request to the FastAPI server
response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print("Response from server:")
    print(response.json())
else:
    # Print an error message
    print(f"Error: {response.status_code}")
    print(response.text)
