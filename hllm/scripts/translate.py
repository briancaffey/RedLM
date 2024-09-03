import os
import json
import openai

# Set the OpenAI API key
openai.api_key = 'your-api-key-here'  # Replace with your OpenAI API key
openai.api_base = 'http://localhost:8000/v1'  # Set to your local server

def split_chinese_sentences(text):
    sentences = []
    sentence = ""

    for char in text:
        sentence += char
        if char == "。":  # Check if the character is a Chinese period
            sentences.append(sentence)
            sentence = ""

    # Add any remaining sentence that does not end with "。"
    if sentence:
        sentences.append(sentence)

    return sentences

def translate_chinese_paragraph(text, target):
    return "".join([translate_text(sentence, target=target) for sentence in split_chinese_sentences(text)])

def translate_text(text, target):
    """
    Rewrite Baihua as modern Mandarin Chinese using few-shot prompting
    """
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", "None"),
        base_url='http://localhost:8000/v1'
    )

    if target == "mandarin":
        # few-shot prompting
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "您是一位中国文学学者，直接将白话文翻译成现代汉语。"
                },
                {
                    "role": "user",
                    "content": "看官！你道此书从何而起？说来虽近荒唐，细玩颇有趣味。"
                },
                {
                    "role": "assistant",
                    "content": "读者朋友，你想知道这本书是怎么开始的吗？说起来虽然有些离奇，但仔细品味却很有意思。"
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model="01-ai/Yi-1.5-6B-Chat",
        )
    # english
    else:
        # few-shot prompting
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a Chinese translator and your task is to directly translate Chinese text into English."
                },
                {
                    "role": "user",
                    "content": "读者朋友，你想知道这本书是怎么开始的吗？说起来虽然有些离奇，但仔细品味却很有意思。"
                },
                {
                    "role": "assistant",
                    "content": "Dear reader, do you want to know how this book begins? Although the story may seem a bit strange at first, it's quite interesting when you take the time to savor it."
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model="01-ai/Yi-1.5-6B-Chat",
        )
    translated_text = response.choices[0].message.content.strip()
    return translated_text

def translate_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for paragraph in data.get("paragraphs", []):
        original_text = paragraph.get("original")
        if original_text:
            translated_text = translate_chinese_paragraph(original_text, target="mandarin")
            paragraph["mandarin"] = translated_text
            print("Baihua\n")
            print(translated_text)
            translated_english_text = translate_chinese_paragraph(translated_text, target="english")
            paragraph["english"] = translated_english_text
            print("English\n")
            print(translated_english_text)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def translate_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(f"Translating: {file_path}")
                translate_json_file(file_path)
                print(f"Translated: {file_path}")
            break


directory_to_translate = "data/book"
translate_directory(directory_to_translate)


# translate_text("此开卷第一回也。作者自云曾历过一番梦幻之后，故将真事隐去，而借“通灵”说此《石头记》一书也，故曰“甄士隐”云云。但书中所记何事何人？自己又云：今风尘碌碌，一事无成，忽念及当日所有之女子，一一细考较去，觉其行止见识皆出我之上，我堂堂须眉，诚不若彼裙钗。我实愧则有馀，悔又无益，大无可如何之日也！当此日，欲将已往所赖天恩祖德锦衣纨袴之时，饫甘餍肥之日，背父兄教育之恩，负师友规训之德，以致今日一技无成，半生潦倒之罪，编述一集，以告天下。知我之负罪固多，然闺阁中历历有人，万不可因我之不肖自护己短，一并使其泯灭也。所以蓬牖茅椽，绳床瓦灶，并不足妨我襟怀。况那晨风夕月，阶柳庭花，更觉得润人笔墨。我虽不学无文，又何妨用假语村言敷衍出来，亦可使闺阁昭传，复可破一时之闷，醒同人之目，不亦宜乎？故曰“贾雨村”云云。更于篇中间用“梦”“幻”等字，却是此书本旨，兼寓提醒阅者之意。")


# TEXT = "此开卷第一回也。作者自云曾历过一番梦幻之后，故将真事隐去，而借“通灵”说此《石头记》一书也，故曰“甄士隐”云云。但书中所记何事何人？自己又云：今风尘碌碌，一事无成，忽念及当日所有之女子，一一细考较去，觉其行止见识皆出我之上，我堂堂须眉，诚不若彼裙钗。我实愧则有馀，悔又无益，大无可如何之日也！当此日，欲将已往所赖天恩祖德锦衣纨袴之时，饫甘餍肥之日，背父兄教育之恩，负师友规训之德，以致今日一技无成，半生潦倒之罪，编述一集，以告天下。知我之负罪固多，然闺阁中历历有人，万不可因我之不肖自护己短，一并使其泯灭也。所以蓬牖茅椽，绳床瓦灶，并不足妨我襟怀。况那晨风夕月，阶柳庭花，更觉得润人笔墨。我虽不学无文，又何妨用假语村言敷衍出来，亦可使闺阁昭传，复可破一时之闷，醒同人之目，不亦宜乎？故曰“贾雨村”云云。更于篇中间用“梦”“幻”等字，却是此书本旨，兼寓提醒阅者之意。"
# TEXT = "此开卷第一回也。作者自云曾历过一番梦幻之后，故将真事隐去，而借“通灵”说此《石头记》一书也，故曰“甄士隐”云云。"
# TEXT = "但书中所记何事何人？自己又云：今风尘碌碌，一事无成，忽念及当日所有之女子，一一细考较去，觉其行止见识皆出我之上，我堂堂须眉，诚不若彼裙钗。"

# TEXT = "我实愧则有馀，悔又无益，大无可如何之日也！当此日，欲将已往所赖天恩祖德锦衣纨袴之时，饫甘餍肥之日，背父兄教育之恩，负师友规训之德，以致今日一技无成，半生潦倒之罪，编述一集，以告天下。"

# TEXT = "知我之负罪固多，然闺阁中历历有人，万不可因我之不肖自护己短，一并使其泯灭也。"
# print("Original Baihua")
# print()
# print(TEXT)
# print()
# print("Mandarin")
# print()
# mandarin_text = translate_text(TEXT, target="mandarin")
# print()
# print("English")
# print()
# translate_text(mandarin_text, target="english")
# # print()
# print()
# print(TEXT)
# print()
# mandarin = translate_chinese_paragraph(TEXT, target="mandarin")
# print(mandarin)
# print()
# english = translate_chinese_paragraph(TEXT, target="english")
# print(english)
# print()