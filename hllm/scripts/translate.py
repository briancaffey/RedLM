import os
import json
import openai

# Set the OpenAI API key
openai.api_key = 'your-api-key-here'  # Replace with your OpenAI API key
openai.api_base = 'http://localhost:8000/v1'  # Set to your local server

def translate_text(text, target_language="English"):
    prompt_template = f"Translate the following text to {target_language}:\n\n{{}}"
    prompt = prompt_template.format(text)

    response = openai.Completion.create(
        engine="text-davinci-003",  # You might need to adjust this based on your server
        prompt=prompt,
        max_tokens=1000
    )

    translation = response.choices[0].text.strip()
    return translation

def translate_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for paragraph in data.get("paragraphs", []):
        original_text = paragraph.get("original")
        if original_text:
            translated_text = translate_text(original_text)
            paragraph["translated"] = translated_text

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def translate_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                translate_json_file(file_path)
                print(f"Translated: {file_path}")

# Example usage
directory_to_translate = "data/book"  # Replace with your directory path
translate_directory(directory_to_translate)
