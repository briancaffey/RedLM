"""
This script asks multiple choice questions to the RAG query engine
"""

import os
import json
import openai

import requests
import json

# Server URL
url = "http://localhost:8080/query"


# Function to format the question and choices
def format_question(q):

    question = q["question"]
    choices = q["choices"]
    formatted_choices = "\n".join([f"{choice[0]}、 {choice[1]}" for choice in choices])
    formatted_question = f"{question}\n{formatted_choices}"

    return formatted_question


# Read JSON data from the file
with open("questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)


def take_test(data):
    num_questions = len(data)
    correct = 0

    for i, q in enumerate(data):

        query = format_question(q)
        payload = {"query": query}

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

        if q["answer"].lower() in response.text.lower():
            correct += 1
            print("✅")
        else:
            print("❌")

        percent = correct / (i + 1)
        print(f"{correct}/{i+1} - Score: {percent:.2f}%")


take_test(data)
