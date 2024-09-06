import requests
import json

# Server URL
url = "http://localhost:8080/query"

# Sample query
# query = "宝玉不知道以下何种农耕作物之名？"
# TODO: adjust RAG template
query = """
        "question": "秦钟的父亲是如何死的？[1分]",
        "choices": [
            [
                "A",
                "外感风寒、风毒之症"
            ],
            [
                "B",
                "被智能儿气死的"
            ],
            [
                "C",
                "生气引发旧病加重"
            ],
            [
                "D",
                "生气而诱发中风而死"
            ]
        ],
"""

# Prepare the request payload
payload = {
    "query": query
}

# Send the POST request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    result = response.json()

    print("Query:", query)
    print("Response:", result["response"])
else:
    print("Error:", response.status_code, response.text)