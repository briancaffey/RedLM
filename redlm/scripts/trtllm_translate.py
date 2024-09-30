import os
import json

from tensorrt_llm import LLM, SamplingParams
from tensorrt_llm.hlapi import BuildConfig


def main():
    # models to use
    # Qwen/Qwen2-7B-Instruct
    # baichuan-inc/Baichuan2-13B-Chat
    MODEL = "Qwen/Qwen2-7B-Instruct"

    # Version is "original" | "english" | "mandarin"
    VERSION = "original"

    bh_to_zh = "把下面的白话写成用简单的现代汉语的句子：\n\n"
    zh_to_en = "Translate the following from Chinese to English:\n\n"

    def get_chapter_data(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=2048)
    build_config = BuildConfig(max_seq_len=4096)

    llm = LLM(model=MODEL, build_config=build_config, tensor_parallel_size=4)

    directory_path = "data/book"
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(f"Translating: {file_path}")

                # get paragraphs to translate
                chapter_data = get_chapter_data(file_path)
                chapter_paragraphs = chapter_data.get("paragraphs", [])
                paragraphs = [p["original"] for p in chapter_paragraphs]

                # bai hua to chinese
                prompts = [f"{bh_to_zh}{p}\n\n" for p in paragraphs]
                # TODO: fix failures where context is exceeded
                try:
                    chinese_outputs = llm.generate(prompts, sampling_params)
                except:
                    continue
                chinese_paragraphs = [
                    output.outputs[0].text for output in chinese_outputs
                ]

                # chinese to english
                prompts = [f"{zh_to_en}{p}\n\n" for p in chinese_paragraphs]
                try:
                    english_outputs = llm.generate(prompts, sampling_params)
                except:
                    continue
                english_paragraphs = [
                    output.outputs[0].text for output in english_outputs
                ]

                # add chinese and english translations to chapter_data
                all_paragraphs = [
                    {**og_dict, "english": en_val, "chinese": cn_val}
                    for og_dict, en_val, cn_val in zip(
                        chapter_paragraphs, english_paragraphs, chinese_paragraphs
                    )
                ]

                chapter_data["paragraphs"] = all_paragraphs

                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(chapter_data, file, ensure_ascii=False, indent=4)

                print(f"Translated: {file_path}")


# Refer to https://mpi4py.readthedocs.io/en/stable/mpi4py.futures.html#mpipoolexecutor
if __name__ == "__main__":
    main()
