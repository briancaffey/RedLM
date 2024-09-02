import requests
from bs4 import BeautifulSoup
import os
import json

# Function to scrape a single chapter
def scrape_chapter(chapter_number):
    url = f"https://ctext.org/hongloumeng/ch{chapter_number}/zhs"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the title from the h2 element inside a td element
    title_element = soup.find('h2')
    title = title_element.get_text(strip=True) if title_element else f"Chapter {chapter_number}"

    # Find all `td` elements with the class `ctext` and exclude those with the class `opt`
    td_elements = soup.find_all('td', class_='ctext')
    data = [{"original": td.get_text(strip=True)} for td in td_elements if 'opt' not in td.get('class', [])]

    # Structure the JSON data
    chapter_data = {
        "paragraphs": data,
        "title": title,
        "chapter_number": chapter_number
    }

    # Create the directory if it doesn't exist
    os.makedirs(f"data/book", exist_ok=True)

    # Save the data as a JSON file
    with open(f"data/book/{chapter_number}.json", "w", encoding='utf-8') as f:
        json.dump(chapter_data, f, ensure_ascii=False, indent=4)

# Loop over the chapters
for i in range(1, 121):
    scrape_chapter(i)
    print(f"Chapter {i} scraped and saved.")
