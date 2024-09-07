import os
import json

# Define the path to the folder containing the JSON files
folder_path = '/home/brian/github/HLLM/hllm/data/book'
output_file = 'chapter_data.json'
chapter_data = []

with open("/home/brian/github/HLLM/hllm/chapter_data.json", 'r') as f:
    image_data = json.load(f)

# Loop over every file in the folder
for i in range(1, 121):

    file_path = os.path.join(folder_path, f"{i}.json")

    # Open and read the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Get the "title" value from the JSON object
    title = data.get('title', 'Untitled')

    # Create the object with "title" and "images" fields
    chapter_entry = {
        "title": title,
        "images": image_data[i-1]["images"]
    }

    # Append to the list
    chapter_data.append(chapter_entry)

# Save the array of objects to chapter_data.json
with open(output_file, 'w') as out_file:
    json.dump(chapter_data, out_file, ensure_ascii=False, indent=4)

print(f'Successfully saved data to {output_file}')
