"""
This script asks multiple choice questions to the LLM and parses the answer
"""

import os
import json
import openai

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", "None"),
    base_url='http://localhost:8000/v1'
)

# Function to format the question and choices
def format_question(q):

    question = q['question']
    choices = q['choices']
    formatted_choices = "\n".join([f"{choice[0]}、 {choice[1]}" for choice in choices])
    formatted_question = f"{question}\n{formatted_choices}"

    return formatted_question

# Read JSON data from the file
with open('questions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def take_test(data):
    num_questions = len(data)
    correct = 0

    for q in data:
        # create a prompt to get the answer choice as a letter
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "请回答问题。不要解释你的答案，只需说明哪个选项是正确答案。"
                },
                {
                    "role": "user",
                    "content": format_question(q),
                }
            ],
            model="01-ai/Yi-1.5-9B-Chat",
        )

        llm_answer = response.choices[0].message.content.strip()
        print(llm_answer)


        if q["answer"].lower() in llm_answer.lower():
            correct += 1
            print("CORRECT")
        else:
            print("____WRONG____")

        print(correct)

    print(f"Answered {correct} questions correctly out of {num_questions}")

take_test(data)