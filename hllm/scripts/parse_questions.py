from bs4 import BeautifulSoup
import json

def parse_html_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    questions = []

    # Find all the question containers
    question_containers = soup.find_all('div', class_='singleContainer')

    for container in question_containers:
        # Extract the question text
        question_text = container.find('div', class_='subjectBox').get_text(strip=True)

        # Extract the choices
        choices = []
        correct_answer = None

        checkboxes = container.find_all('div', class_='checkBox')
        answers = []
        for checkbox in checkboxes:
            # Extract the option letter (A, B, C, etc.)
            option_letter = checkbox.find('div', class_='dijitReset dijitInline').get_text(strip=True)
            # Extract the option content (the text of the option)
            option_content = checkbox.find('div', class_='optionContent').get_text(strip=True)
            choices.append([option_letter, option_content])

            # Check if this option is the correct answer
            if checkbox.find('div', class_='dijitCheckBoxCheckedDisabled'):
                answers.append(option_letter)
                correct_answer = option_letter

        # Store the question, choices, and correct answer
        question_data = {
            "question": question_text,
            "choices": choices,
            "answer": correct_answer
        }
        if len(answers) == 1:
            questions.append(question_data)

    return questions

def save_questions_to_json(questions, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    questions = parse_html_file('questions.html')
    print(f"Parsed {len(questions)}")
    save_questions_to_json(questions, 'questions.json')
