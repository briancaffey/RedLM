import os
import json

from tensorrt_llm import LLM, SamplingParams
from tensorrt_llm.hlapi import BuildConfig


def main():
    """
    Main function for translating
    """

    def split_chinese_text(text, min_length=300):
        """
        Helper function to split long paragraphs into substrings based on Chinese punctuation
        This ensures that all completion prompts for translation stay within the context window of the LLM
        """
        result = []
        current_segment = []
        length = 0

        # Helper function to append segment to result
        def append_segment():
            if current_segment:
                result.append(''.join(current_segment))

        for idx, char in enumerate(text):
            current_segment.append(char)
            length += 1

            # Check if the current character is a Chinese period
            if char == "。" or char == "？":
                # Check the next character to ensure it's not "“"
                if idx + 1 < len(text) and text[idx + 1] == "“":
                    continue

                # If the current segment length exceeds the minimum length
                if length >= min_length:
                    append_segment()
                    current_segment = []  # Reset segment
                    length = 0

        # Append any remaining text
        if current_segment:
            append_segment()

        return result

    def combine(flat, structured):
        """
        Helper function that helps keep all completion prompts inside the context window
        It recombines text paragraph after parallel translation occurs
        The structured list contains strings and lists of strings:
            - strings are used when the paragraph is small enough to fit in context length
            - list of strings are used when a paragraph is split up into subsections
            - these subsections need to be combined into single paragraphs after translation
        The flat list is a list of strings that is sent directly to the LLM for completion inference

        The returned value is a list of paragraphs. The
        """
        output = []
        t = 0
        s = 0

        while t < len(flat) and s < len(structured):

            if type(structured[s]) == str:
                to_append = flat[t]
                output.append(to_append)
                s += 1
                t += 1

            else:
                count = len(structured[s])
                to_append = flat[t:t+count]
                output.append(to_append)
                t += count
                s += 1

        ret = ["".join(o) if type(o) == list else o for o in output]
        return ret

    def process_strings(string_list, target_len):
        """
        This function takes a list of paragraphs and returns a list composed of strings and lists of strings
        This is a helper function for keeping the translation prompts inside the context window

        For example, suppose the following:
        target_len = 5
        string_list = ["abc", "defghijklmn", "xyz"]

        The function will return the following values:

        flat: ["abc", "defgh", "ijklm", "n", "xyz"] # strings in this list have len(string) <= target_len
        substrings: ["abc", ["defgh", "ijklm", "n"], "xyz"]

        The "flat" list is sent to the LLM for translation, and a flat list of translated text is returned from the LLM
        When it is returned, the flat list is reconstructed. For simplicity, assume "translation" is capitalization

        flat_translated: ["ABC", "DEFGH", "IJKLM", "N", "XYZ"]
        this is then transformed into: ["ABC", ["DEFGH", "IJKLM", "N"], "XYZ"]
        which is finally returned into the translated paragraphs: ["ABC", "DEFGHIJKLMN", "XYZ"]

        This function only takes care of part of this process:
        ["abc", "defghijklmn", "xyz"] => ["abc", "defgh", "ijklm", "n", "xyz"], ["abc", ["defgh", "ijklm", "n"], "xyz"]
        original list of strings => flat, substrings
        TODO: rename the variable substrings
        """
        # Initialize empty lists
        substrings = []
        flat = []

        # Loop over the input list
        for s in string_list:
            if len(s) < target_len:
                # Append string to both lists
                substrings.append(s)
                flat.append(s)
            else:
                # Split the long Chinese paragraph into chunks
                split_string = split_chinese_text(s)
                substrings.append(split_string)
                flat.extend(split_string)

        # Return the flat list and substrings list
        return flat, substrings

    # models to use
    # Qwen/Qwen2-7B
    # baichuan-inc/Baichuan2-13B-Base
    MODEL = "Qwen/Qwen2-7B"

    # Version is "original" | "english" | "mandarin"
    VERSION = "original"

    bh_to_zh = "请将下面的白话文段落改写为简单的现代汉语：\n\n"
    zh_to_en = "Translate the following Chinese text to English:\n\n"

    def get_chapter_data(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    sampling_params = SamplingParams(temperature=.7, top_p=0.95, max_tokens=256)
    build_config = BuildConfig(max_seq_len=2048)

    llm = LLM(model=MODEL, build_config=build_config, tensor_parallel_size=4)

    directory_path = "data/book"
    for i in range(1, 121):

        file_path = os.path.join(directory_path, f"{i}.json")
        print(f"Translating: {file_path}")

        # get paragraphs to translate
        chapter_data = get_chapter_data(file_path)
        chapter_paragraphs = chapter_data.get("paragraphs", [])
        paragraphs = [p["original"] for p in chapter_paragraphs]

        # split paragraphs
        flat_bai, structured_bai = process_strings(paragraphs, 300)

        # bai hua to chinese
        # bai_prompts = [f"{bh_to_zh}{p}\n\n" for p in flat_bai]
        bai_prompts = [f"以下是如何将中国白话改写为简单的现代普通话的示例。\n\n中国白话：\n\n{p}\n\n简单的现代普通话：\n\n" for p in flat_bai]
        # TODO: fix failures where context is exceeded
        
        max_input_len = max([len(p) for p in bai_prompts])
        print(f"Max length of bai input prompts {max_input_len}")

        try:
            chinese_outputs = llm.generate(bai_prompts, sampling_params)
        except Exception as e:
            print("############## Exception ###############")
            print(e)
            continue
        chinese_paragraphs = [
            output.outputs[0].text for output in chinese_outputs
        ]
        
        max_len = max([len(p) for p in chinese_paragraphs])
        print(f"Maximum length of translated text: {max_len}")

        # combine flat paragraphs and paragraph fragments to list of paragraphs
        complete_chinese_paragraphs = combine(chinese_paragraphs, structured_bai)

        # prepare Mandarin Chinese paragraphs for translation to English
        flat_mandarin, structured_mandarin = process_strings(complete_chinese_paragraphs, 300)

        # chinese to english
        # prompts = [f"{zh_to_en}{p}\n\n" for p in flat_mandarin]
        prompts = [f"中文原文：\n\n{p}\n\n英文翻译：\n\n" for p in flat_mandarin]
        try:
            english_outputs = llm.generate(prompts, sampling_params)
        except Exception as e:
            print("############## Exception in English translation ###############")
            print(e)
            continue
        english_paragraphs = [
            output.outputs[0].text for output in english_outputs
        ]



        complete_english_paragraphs = combine(english_paragraphs, structured_mandarin)

        # add chinese and english translations to chapter_data
        all_paragraphs = [
            {**og_dict, "english": en_val, "chinese": cn_val}
            for og_dict, en_val, cn_val in zip(
                chapter_paragraphs, complete_english_paragraphs, complete_chinese_paragraphs
            )
        ]

        chapter_data["paragraphs"] = all_paragraphs

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(chapter_data, file, ensure_ascii=False, indent=4)

        print(f"Translated: {file_path}")


# Refer to https://mpi4py.readthedocs.io/en/stable/mpi4py.futures.html#mpipoolexecutor
if __name__ == "__main__":
    main()
