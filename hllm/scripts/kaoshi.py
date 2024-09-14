"""
This script asks multiple choice questions to the LLM and parses the answer
"""

import os
import json
from llama_index.llms.openai_like import OpenAILike

model = OpenAILike(
    model="01-ai/Yi-1.5-9B-Chat",
    api_base="http://localhost:8000/v1",
    api_key="None",
    # keep this number small since we don't need a long explination for multiple-choice test evaluation
    max_tokens=16,
)


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
        response = model.complete(prompt=query)

        print(query)
        print(response.text)

        if q["answer"].lower() in response.text.lower():
            correct += 1
            print("✅")
        else:
            print("❌")

        percent = correct / (i + 1)
        print(f"{correct}/{i+1} - Score: {percent*100:.2f}%")
        print()

    print(f"Answered {correct} questions correctly out of {num_questions}")


take_test(data)
