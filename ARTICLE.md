---
title: "RedLM: My submission for the NVIDIA and LlamaIndex Developer Contest"
date: '2024-10-2'
description: "RedLM is an AI-powered application for the study of China's greatest classical novel: Dream of the Red Chamber"
image: /static/redlm/title.png
tags:
  - nvidia
  - llama-index
  - ai
  - llm
  - rag
  - tensorrt-llm
  - chinese

draft: true

# external:
#   - link: https://x.com/briancaffey/
#     site: x

comments: true
---

## td;dr

RedLM is a new way to study art and literature powered by artificial intelligence. It is an application that applies LLMs to the study of one of China’s most famous literary works: Dream of the Red Chamber. It uses leading Chinese language models and vision language models from Chinese AI groups including Alibaba’s Qwen team, Baichuan Intelligence Technology and 01.AI. RedLM uses tools, techniques and services from NVIDIA and LlamaIndex including NVIDIA NIMs, Retrieval Augmented Generation and Multi-Modal RAG with vision language models. This project is my submission for the NVIDIA and LlamaIndex Developer Contest.

There are This article will cover how I built the project, challenges I faced and some of the lessons I learned while working with NVIDIA and LlamaIndex technologies.

## What is RedLM?

RedLM is a combination of the word “Red” and LM, an abbreviation for “language model”. Dream of the Red Chamber is such an important book in Chinese literature that it has its own field of study called 红学 (literally “the study of red”), or Redology. So, RedLM is an application that uses language models for the study of Redology.

![RedLM](/static/redlm/title.png)

In this project I focused on three applications of language models:

1. Summary and translation of the source text
2. A Q&A bot that can answer questions about the book providing references to the specific paragraphs used to give answers
3. An image-based Q&A bot that can answer questions about sections of paintings that depict scenes from each of the book’s chapters.

## NotebookLM

I took this article and fed it to NotebookLM to create a short podcast-style dialog that describes the project:

![NotebookLM](/static/redlm/notebooklm.png)

## How I built RedLM

The core application consists of two parts: a web UI built with Nuxt and Vue 3 and a backend API built with FastAPI and LlamaIndex. There are lots of great tools for building full-stack AI applications such as Gradio and Streamlit, but I wanted to build with the web tools that I’m most familiar with and that provide the most flexibility. These frameworks (Nuxt and FastAPI) are simple and effective and they allowed me to develop quickly. Most of the code for this project was written by AI. I used OpenAI’s ChatGPT 4o, Anthropic’s Claude 3.5 Sonnet and 01.AI’s Yi-1.5-9B-Chat model. This means that I could write a prompt for a single-file-component in Vue or an API route for FastAPI and get perfectly-written code often on the first prompt.

This project supports hybrid AI inference, meaning that the AI inference can be done either on local RTX PCs or using NVIDIA’s Cloud APIs from `build.nvidia.com`. I used PCs with NVIDIA GeForce RTX 4090 GPUs to do inference with language and vision models, and with a change of configuration, I was able to do the same inference using NVIDIA’s API endpoints.

## Translating Dream of the Red Chamber with TensorRT-LLM

Translation is often mentioned as one of the capabilities of bilingual LLMs from China. I wanted to try translating this book from Chinese to English, but I also wanted to better understand the meaning of the original text written in vernacular Chinese.

I decided to try both: first, I used LLMs to rewrite the original text in simple, modern Mandarin Chinese and then second, I translated the modern Mandarin version into English.

Dream of the Red Chamber is a large book. It is composed of over 800,000 Chinese characters, using 4303 unique Chinese characters. It has 120 chapters and a total of 3996 paragraphs. Here is a histogram showing the number of characters per paragraph.

![Paragraph lengths](/static/redlm/paragraphs.png)

I rented a large multi-GPU instance from AWS using some of the credits I get as a member of the AWS Community Builders program. The g5.12xlarge instance I selected has 4 A10G Tensor Core GPUs. The TensorRT-LLM LLM API is a relatively new part of the TensorRT-LLM library. It provides a very simple, high-level interface for doing inference. Following the [LLM Generate Distributed example](https://nvidia.github.io/TensorRT-LLM/llm-api-examples/llm_generate_distributed.html) from the TensorRT-LLM documentation, I was able to translate the entire book into simple Mandarin and then from Mandarin into English in about an hour and 15 minutes.

```
Translating: data/book/22.json
Processed requests: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 38/38 [00:15<00:00,  2.41it/s]
Processed requests: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 38/38 [00:24<00:00,  1.54it/s]
Translated: data/book/22.json
Translating: data/book/114.json
Processed requests: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 20/20 [00:11<00:00,  1.81it/s]
Processed requests: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 20/20 [00:12<00:00,  1.58it/s]
Translated: data/book/114.json
[TensorRT-LLM][INFO] Refreshed the MPI local session
[TensorRT-LLM][INFO] Refreshed the MPI local session
[TensorRT-LLM][INFO] Refreshed the MPI local session
[TensorRT-LLM][INFO] Refreshed the MPI local session

real	74m1.578s
user	0m45.936s
sys	0m36.283s
```

Getting good results required a bit of experimentation with parameters. The LLM API makes this very easy. The following code configures settings and builds the inference engine that can be used for doing completions:

```python
sampling_params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=256)
build_config = BuildConfig(max_seq_len=2048)
llm = LLM(model=MODEL, build_config=build_config, tensor_parallel_size=4)
```

I used the following prompts to rewrite each paragraph of the original text in simple, modern Mandarin Chinese:

```python
bai_prompts = [
    # Here are examples of how to rewrite Chinese vernacular into simple modern Mandarin.\n\nChinese vernacular:\n\n{p}\n\nSimple modern Mandarin
    f"以下是如何将中国白话改写为简单的现代普通话的示例。\n\n中文白话：\n\n{p}\n\n简单的现代普通话：\n\n"
    for p in flat_bai
]
```

It was difficult to get good results consistently. Here are some observations I had:

- Some of the translated paragraphs were perfect
- some translated paragraphs would randomly hallucinate the same phrase over and over again
- Some requests to translate text to English would reply in Mandarin Chinese rather than in English
- Sometimes I would even see code generated when asking for a translation
- The names of characters were sometimes translated inconsistently.

ChatGPT 4o in my experience could handle any translation task flawlessly, but the `Qwen2-7B` model I used had mixed results! The change that I made that seemed to have the biggest impact on translation quality was setting `*max_tokens*=256` in `SamplingParams`. I probably could have used a dynamic value for `max_tokens` based on the size of the current paragraph being translated. I also would have like to set up side-by-side comparisons of translations using different sized models, but rather than spend time on optimizing translation with TensorRT-LLM, I wanted to focus on the main part of this project: Retrieval Augmented Generation with LlamaIndex.

## Building Q&A bots with RAG using LlamaIndex

My primary object with this project was to implement a simple chat feature that responds to questions about the book with relevant responses including the references to the specific paragraphs used in the response. The following shows images of the UI I built with one of the examples I included in the video I made for this project.

![RAG Example](/static/redlm/rag_example.png)

The question in the screenshots above is: “What does Jia Baoyu’s father think about him?” The response includes references to paragraphs where Jia Zheng (Baoyu’s father) is discussing his son. I was pretty amazed that the RAG query was able to pull out these two paragraphs. I haven’t read very much of this book at all, but the retrieved documents seemed to be directly related to my query.

By default, LlamaIndex uses cosine similarity as the distance metric for find the vectors representing the documents (paragraphs) that are “closest” to the vector representing the user query.

![Cosine Similarity](/static/redlm/cosine_similarity.png)

Source: https://medium.com/@kbdhunga/a-beginners-guide-to-similarity-search-vector-indexing-part-one-9cf5e9171976

Here is some of the code I wrote for this feature that uses LlamaIndex’s `CustomQueryEngine` to fetch the “nodes” from which I get the referenced paragraph text, chapter number and paragraph number.

```python

# the prompt used in the query engine below with English translation in the comments
q_and_a_prompt = PromptTemplate(
    "这是相关的参考资料：\n" # Here is some related reference material:
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "根据上述的参考资料，回答下面的问题\n" # Based on the above reference material, answer the following question:
    "问题：{query_str}\n" # Question:
)


class QAndAQueryEngine(CustomQueryEngine):
    """RAG Completion Query Engine optimized for Q&A"""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAILike
    qa_prompt: PromptTemplate

    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)
        metadata = []
        # Collect the metadata into a list of dicts so that it can be sent to UI for references
        for node in nodes:
            metadata_dict = {}
            node_metadata = node.node.metadata
            metadata_dict["content"] = node.node.text
            metadata_dict["chapter"] = int(node_metadata.get("chapter"))
            metadata_dict["paragraph"] = int(node_metadata.get("paragraph"))

            metadata.append(metadata_dict)

        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        response = self.llm.chat(
            [
                ChatMessage(
                    role="user",
                    content=q_and_a_prompt.format(
                        context_str=context_str, query_str=query_str
                    ),
                )
            ]
        )

        return response, metadata
```

This chapter number and paragraph number are added to the document as metadata during the indexing step which I run once via a script before starting the FastAPI server.

## RedLM RAG Evaluation

Once I got the Q&A bot set up with RAG I wanted to find a way to test it. I heard that the novel Dream of the Red Chamber is studied widely in Chinese schools, so I searched around for a set of multiple choice questions.

This search led me to find [a set of 1000 multiple choice questions about Dream of the Red Chamber on examcoo.com](https://www.examcoo.com/editor/do/view/id/246401). I wrote a script to parse the questions from the website HTML using ChatGPT (parsing is one of my favorite use cases of coding LLMs!) I filtered out questions based on the following criteria:

- Four answer choices - some of the questions had more than four answer choices. I filtered questions with more than four answer choices to keep the evaluation simple. This would allow me to assume that random answer choices would have a 25% chance of being correct.
- Only one answer - some questions had more than one answer. This would also help keep the evaluation logic simple.

![Multiple Choice Questions from Dream of the Red Chamber Test](/static/redlm/hlm_mcq.png)

Multiple choice questions from a Dream of the Red Chamber test (examcoo.com)

To run the evaluation I set up two scripts. The first script would prompt the LLM to answer the question without any additional information from the RAG system. This served as a baseline to see how well the LLM could do at answering multiple choice questions. The script checks to see if the LLM response contains the letter (A, B, C or D) of the correct answer and keeps track of the number of questions answered correctly.

Another script was used to test ability of the LLM using RAG. In this script, the prompt sent to the LLM included relevant paragraphs from the book.

Here are some results and other observations from this experiment:

- LLMs alone scored in the mid 30% range (36%)
- LLMs using retrieval augmented generation with the set of questions score in the mid 40% range (44%)
- I used a the completion API rather than the chat API and set the `max_tokens` to 16. This was done to ensure that the LLM only gave a short response with a valid answer choice rather than giving a long response with an explanation.
- The evaluation took longer for LLM + RAG test because of the time required for making the RAG query and the longer prompt (including both the original multiple-choice question and the referenced paragraphs).
- I used the `01-ai/Yi-1.5-9B-Chat` model for this test, but I probably should have used the base model rather than the chat model.
- Some questions would not be capable of being answered by RAG. For example, some of the questions are about film renditions of the novel. Most of the questions seemed relevant to the content of the book, so I didn’t bother to filter out the questions that were not directly related to the book’s content.

Here is an example of a question that the LLM test script answered incorrectly and the LLM + RAG test script answered correctly.

> 秦钟的父亲是如何死的？
>
> A、外感风寒、风毒之症
>
> B、被智能儿气死的
>
> C、生气引发旧病加重
>
> D、生气而诱发中风而死

Translation:

>How did Qin Zhong's father die?
>
>**A.** He caught a cold and developed wind-related illnesses.
>
>**B.** He was angered to death by Zhineng'er (a character).
>
>**C.** His old illness worsened due to anger.
>
>**D.** He had a stroke induced by anger and died.

Here is the paragraphs that the RAG query returned along with the English translation:

Original
> 荣两处上下内外人等莫不欢天喜地，独有宝玉置若罔闻。你道什么缘故？原来近日水月庵的智能私逃入城，来找秦钟，不意被秦邦业知觉，将智能逐出，将秦钟打了一顿，自己气的老病发了，三五日便呜呼哀哉了。秦钟本自怯弱，又带病未痊，受了笞杖，今见老父气死，悔痛无及，又添了许多病症。因此，宝玉心中怅怅不乐。虽有元春晋封之事，那解得他的愁闷？贾母等如何谢恩，如何回家，亲友如何来庆贺，宁荣两府近日如何热闹，众人如何得意，独他一个皆视有如无，毫不介意。因此，众人嘲他越发呆了。

English
> Everyone in the Rong and Ning households, both inside and outside, were extremely happy, except for Baoyu, who seemed indifferent. Do you want to know why? It turns out that recently, the nun Zhineng from Shuiyue Temple secretly ran into the city to find Qin Zhong. Unexpectedly, she was discovered by Qin Zhong's father, Qin Banger. Qin Banger not only drove Zhineng away but also gave Qin Zhong a beating. This made Qin Banger so angry that his old illness relapsed, and within three to five days, he passed away. Qin Zhong had always been weak and hadn't fully recovered from a previous illness. After being beaten and seeing his father die in anger, he was overwhelmed with regret and sorrow, which worsened his condition. As a result, Baoyu felt very melancholic. Although the promotion of Yuan Chun to imperial concubine was a joyful event, it couldn't alleviate the gloom in his heart. While Grandmother Jia and others were busy expressing their gratitude and returning home, and relatives and friends came to celebrate, and the Rong and Ning households were bustling with excitement, Baoyu alone remained completely indifferent to it all. Consequently, everyone started to mock him for becoming more and more absent-minded.

The correct answer for this question is C.

## Multi-modal RAG for visual reasoning

Qwen2-VL was released a few days before I heard about this contest. Qwen is the name of Alibaba’s AI Lab, and it is an abbreviation of the Chinese characters: 千问 (”qian wen”, meaning 1000 questions). VL stands for vision-language, meaning that the model is capable of understanding both text and images. I had tested out the previous version of Qwen’s vision-language model and was very impressed by how it could answer questions about images.

Sun Wen was a Qing-era painter who spent 36 years of his life creating a series of 230 paintings detailing scenes from Dream of the Red Chamber. These images are incredibly detailed and often contain multiple disjointed scenes in one painting. If you asked a Qwen-VL model to describe one of the images, you might get back a lengthy description, and the context window might easily be exceeded when including a resolution high enough for the model to properly “see” anything.

This gave me the idea to build a feature where a user can select part of a painting (by clicking and dragging on an image) and ask a question about that section of the painting alone. I knew that this could be done with something like HTML canvas, and I also knew that doing this on my own would take a very long time to write since I am at best a very casual frontend developer. It took me just a few minutes to write out the prompt and Claude 3.5 Sonnet wrote a perfect prototype in less than a minute. Here’s the prompt I used:

> I'm going to describe a Vue component and I want you to write it using Vue 3 to the best of your ability.
>
>
> write a simple single-file vue component using Vue 3 that does the following:
>
> - displays an image
> - allows the users to click and drag to select a subsection of the image
> - the subsection of the image is saved as a base64-encoded data url to a variable that is displayed below the image
>
> The solution should make use of HTML canvas. When you click down on the image you begin selecting the subsection. You then move the mouse to make your subsection on the image, and when you mouse-up the subsection is selected and the data url is updated. Then the subsection is displayed at the very bottom of the page as a "preview" image using the base 64 image string as the image source.
>
> The selection box should be a dashed red line
>

![RedLM Image Q&A](/static/redlm/image-qa.png)

This shows the final result of the UI I built for the image Q&A feature in RedLM. It uses a similar chat layout that the text-based Q&A feature uses, with the addition of the image preview included in the chat log. The user query in this example just says “Please describe the contents of the image”. Here is a diagram showing the overall flow of the image Q&A feature:

![Diagram of RedLM Image Q&A with RAG and Vision Language Models](/static/redlm/redlm.drawio.png)

This flow chart shows how the image Q&A feature works.

1. The user selects part of an image and writes a question. This data is then sent to the RedLM API as a post request to the `/mm-q-and-a` endpoint (multi-modal Q&A).
2. Vision language models are used to get a description of the image. Depending on the application configuration, this query can use models such as `Qwen/Qwen2-VL-2B-Instruct` on RTX PCs or using the NVIDIA API Catalog using larger models such as `meta/llama-3.2-90b-vision-instruct`. Not all vision language models have the same interface, so I added some logic to handle different model formats.
3. The image description is used to fetch relevant documents from the Vector Database
4. The full prompt with the image description and relevant documents is sent to the LLM. Again, inference for this step is done either with RTX PCs or using models from the `build.nvidia.com` API catalog.
5. The response from the LLM is sent back to the browser and is displayed to the user as a chat message.

Here is the prompt I used for the image Q&A feature:

```python
# multi-modla Q&A prompt
mm_q_and_a_prompt = PromptTemplate(
		# "here is relevant content from the book"
    "这是书中相关的内容：\n"
    # the relevant chapters are added here
    "{context_str}\n"
    "---------------------\n"
    "下面是场景的描述：\n" # "below is a description of a scene"
    "---------------------\n"
    # the image description from the vision language model is added here
    "{query_str}\n"
    "---------------------\n"
    # "based on the above information, please explain the relationship between the scene and the book"
    "根据上述的信息，尽量解释上说的场景和书的关系。"
)
```

The prompt engineering for this feature was tricky. I was able to get some awesome results that would give me detailed and accurate responses, and then sometimes the LLM would seem confused about my query and tell me that there was no relationship between the scene description and the book content. Sometimes it would give me an accurate description of the scene, but then proceed to tell me that the book content is not related to the scene at all.

There is another important concept from LlamaIndex that I used to build the image Q&A feature: metadata filtering. Metadata filtering is an important concept in RAG systems  because it helps you focus your query on relevant documents in a precise way. A very simple example might be a RAG system that indexes news articles and stores the associated date as metadata. You could allow a user to set a date range for their query and only include articles that match the given date range.

For my image Q&A system, I have a mapping between the paintings and their associated chapters. When I ask a question about a painting, I want to use the description of the image to find similar paragraphs, but only the paragraphs that occur in the painting’s associated chapter. What I ended up doing was filtering the entire index before making the query. The alternative would be filtering the returned nodes after making the query, but this would have the possibility of not returning any nodes.

Here’s what some of the metadata filtering code looks like:

```python
# main.py
# filter by chapters associated with the queried image
filters = MetadataFilters(
    filters=[ExactMatchFilter(key="chapter", value=str(req_data.chapter))]
)
query_engine = get_query_engine_for_multi_modal(filters)

# rag.py
# utility function that returns the query engine use for image Q&A
# the index is filtered to only include nodes associated with the image being queried
def get_query_engine_for_multi_modal(filters):
    retriever = index.as_retriever(filters=filters)
    synthesizer = get_response_synthesizer(response_mode="compact")
    try:
        query_engine = QAndAQueryEngine(
            retriever=retriever,
            response_synthesizer=synthesizer,
            llm=model,
            qa_prompt=mm_q_and_a_prompt,
        )
    except Exception as e:
        print(e)
    return query_engine
```

This seemed to work well for my use case, but it might not be a best practice, and it might not be efficient at a bigger scale.

## LlamaIndex Developer Experience

Overall, I found the LlamaIndex documentation to be very helpful. Before using LlamaIndex for this project I had used LangChain to build a RAG POC, but I didn’t get very good results. I love how the LlamaIndex documentation has a 5-line starter example for building a RAG system:

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Some question about the data should go here")
print(response)
```

Source: [https://docs.llamaindex.ai/en/stable/#getting-started](https://docs.llamaindex.ai/en/stable/#getting-started)

I was able to expand this simple example to implement the text and image Q&A bots for RedLM fairly easily. The application I built is somewhat similar to the [Full-Stack Web App with LLamaIndex](https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/apps/fullstack_app_guide/) included in their documentation.

## NVIDIA inference stack (TensorRT-LLM and build.nvidia.com)

The LLM API for TensorRT-LLM is a very nice developer experience compared with my earlier attempts with manually building inference engines. The roadmap for TensorRT-LLM looks promising, I’m looking forward to support for an OpenAI Compatible API and more models. NVIDIA NIMs using TensorRT-LLM are an easy way to run models as OpenAI compatible API servers, but the selection of models is still pretty limited. vLLM provides a strong alternative with a wide range of support models. NVIDIA NIMs for LLMs build on vLLM libraries and the TensorRT-LLM library, so it is helpful to have an understanding of both of these libraries to stay on the bleeding edge of performant inference engines.

![trt-llm-roadmap](/static/redlm/trt-llm-roadmap.png)

The NVIDIA API catalog is a great way to test a variety of different models, especially large models that cannot fit into consumer hardware like RTX PCs or high-end MacBooks. I got to try out the new meta/llama-3.2-90b-vision-instruct model in my project by simply changing a value in my .env file, this is a great developer experience!

![build.nvidia.com](/static/redlm/build.nvidia.com.png)

The NVIDIA API catalog doesn’t have every model in every size, however. For example, it has the qwen/qwen2-7b-instruct model, but doesn’t have the qwen/qwen2-7b-instruct model. Also, only some of the models are labeled as “Run Anywhere”; a lot of the models say “Self-Hosted API Coming Soon” meaning that they can’t be downloaded an run locally as a container. To get around this, I ran inferences services locally using both vLLM’s vllm/vllm-openai container and my own container running Qwen and other services.


## My local inference stack (RTX)

![RTX PCs](/static/redlm/rtxpcs.png)

Two of the RTX PCs in my home network: `a1` and `a3`. `a1` was the first PC I built by myself and was the beginning of my GeForce journey. Luckily I built it with an over-provisioned PSU, so it can use a 4090 FE card! The front panel doesn't fit, however.

One limitation of the NVIDIA API catalog is the number of free credits given for a trial account. Using 1 credit per API call, I would use up the 1000 credits very quickly when running scripts like translation or the RAG evaluation. The same would be true with rate limits of the OpenAI API. That’s why running LLMs locally is still an important part of the development cycle for this type of project.


This project primarily uses two models: a large language model and a vision language models. Running the Yi-1.5-9B-Chat model from [01.AI](http://01.AI) takes up just about all of the GPU memory on one of my RTX 4090 PCs, so I had to run the vision model on another PC. In a previous project, I used Kubernetes to manage lots of different inference services: LLMs, ComfyUI, ChatTTS and MusicGen for making AI videos and I found it to a nice way to manage different containerized inference services.

```
brian@a3:~$ microk8s kubectl get no -o wide
NAME   STATUS   ROLES    AGE    VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
a1     Ready    <none>   4d4h   v1.30.5   192.168.5.182   <none>        Ubuntu 24.04.1 LTS   6.8.0-45-generic   containerd://1.6.28
a2     Ready    <none>   11d    v1.30.5   192.168.5.96    <none>        Ubuntu 24.04.1 LTS   6.8.0-45-generic   containerd://1.6.28
a3     Ready    <none>   11d    v1.30.5   192.168.5.173   <none>        Ubuntu 24.04.1 LTS   6.8.0-45-generic   containerd://1.6.28
```

In the RedLM GitHub repo I included kubernetes manifests that show how to run the LLM and VLM across two different computers. I used Kustomize as a way to replace dynamic values in the YAML files for different resources. The kubernetes set up is experimental; the LLM and VLM can more reliably be run with `docker run` commands.

![k8s dashboard for local inference services](/static/redlm/k8s-dashboard.png)

I had a lot of driver issues when trying to get kubernetes to run the vLLM container for the Yi LLM. I struggled with the following error message when trying to run the `vllm` LLM service:

> RuntimeError: Unexpected error from cudaGetDeviceCount(). Did you run some cuda functions before calling NumCudaDevices() that might have already set an error? Error 804: forward compatibility was attempted on non supported HW

I tried uninstalling and reinstalling different versions of the NVIDIA drivers and CUDA but kept seeing the same message once the server would try to start up in the vLLM container logs. Rebooting my PC didn't work either. I saw a recommendation to turn off securet boot in BIOS. I didn't turn it on, but having nothing else to try I went into the BIOS settings and found that there were some keys configured in the secure boot section. After I deleted these keys and reboot, everything seemed to work normally. I'm not sure why my PC was in secure boot mode, though!

## Remote Local Development

I use Tailscale for VPN access into my home network. This allows me to use VSCode to connect to folders on my PCs (Remote-SSH) and also lets me do things like portforwarding. For example, I can run the `microk8s dashboard-proxy` command and then port forward port `10443` to the remote IP for access to the Kubernetes dashboard with the following command:

```
ssh -L 10443:100.69.6.58:10443 brian@100.69.6.58
```

## CloudFlare Tunnels

CloudFlare Tunnels is another product that is helpful for building, testing and sharing applications that run on my RTX PC cluster. It allows me to safely expose a service running on my home network to the public internet. For example, I can point [https://redlm.briancaffey.com](https://redlm.briancaffey.com) to `localhost:3000` where I'm running my Nuxt site locally. This serves traffic through CloudFlare's servers; traffic from the internet does go into my home network. I do this for a number of other services that run on my home PCs, such as image generation, etc.

## The success of Black Myth: Wukong

I originally got the idea to build this project after seeing the release of Black Myth: Wukong. This game is a blockbuster success from a Chinese developer that tells the story of the Monkey King’s adventure in the Journey West universe. Journey West (西游记) is another one of the “Four Great Works” of Chinese literature. It tells the story of the legendary pilgrimage of the monk Xuanzang (also known as Tang Sanzang) to India, accompanied by his three disciples—Sun Wukong (the Monkey King), Zhu Bajie (Pigsy), and Sha Wujing (Sandy). The group travels to retrieve sacred Buddhist scriptures, facing numerous challenges, demons, and supernatural beings along the way.

The novel blends elements of adventure, mythology, and spiritual allegory, with Sun Wukong's mischievous nature and extraordinary powers adding humor and excitement. Through their journey, the characters grow and overcome personal flaws, ultimately achieving enlightenment and spiritual success.

This game has set world records for numbers of concurrent players, and it has rewritten the narrative around what is capable with offline single-player games and on top of that it is developed by an obscure game studio from Shenzhen, China.

![Black Myth: Wukong](/static/redlm/wukong.png)

## RedLM video

I created the video for this project using Blender. Blender is my favorite tool for 3D and its sequencer editor is a great non-linear video editing tool for simple projects. I used the following formula to create the video:

1. Background music: I used the AI music generation service called Suno with the prompt “mystical strange traditional Chinese music from the Qing Dynasty”. Here’s the link to my Suno playlist called “Qing Dynasty Music” where you can find the original song and some other good songs that I generated using this prompt. [TODO: Add Suno playlist link]
2. Outline: For this project, the main sections are the introduction, then explaining each part with a short demo: translation, text-based Q&A, evaluation for text-based Q&A, image-based Q&A, and finally a short outro. I wrote an outline and then ChatGPT helped with filling out the content.
3. Narration: I used ElevenLabs to narrate the main part of the video using a clone of my voice using the ElevenLabs Voice Lab. The Chinese voices were generated on my computer with an open-source text-to-speech model called ChatTTS.
4. Images and videos: I gathered images and screen captures of different parts of the project including code snippets, paintings of the book, flow diagrams and screen recordings of the application.

The video is composed of different “strips”. The green strips represent the music and voice clips. Red strips are images and yellow strips are videos. Here is what the final cut of the video looks like in Blender’s Sequencer view:

![Blender Sequence Editor](/static/redlm/blender_sequence_editor.png)

ChatTTS is one of the most impressive open-source models I have seen for generating conversational speech with prosodic elements (pausing, laughter, etc.) It is developed by a Chinese company called 2noise. Earlier this year I made a small contribution to this project with an API example using FastAPI to show how to run a standalone API using the model. Another example in this project provides a comprehensive example application built with gradio:

![ChatTTS UI](/static/redlm/chattts_ui.png)

I was planning on streaming the narration audio for Q&A answers using my ChatTTS API service, but I didn’t get around to doing this. Instead, I just used the Gradio application to generate the Chinese narration for Q&A and image Q&A examples included in the video.

## Thoughts about this contest

I’m glad to have had the opportunity to join three NVIDIA developer contests this year. I like the idea of a “developer contest” that takes place over several weeks compared to hackathons that take place over just a few days. Having more time allows you to learn about a new tool or framework at a deeper level and think about how to apply it in a creative project.

![NVIDIA and LlamaIndex Contest](/static/redlm/llama-contest-og.jpg)

I also like how this contest is not team based. Working on this project I was able to do a lot of high-level thinking, write out features as detailed prompts, and then delegate the code writing to LLMs as if I was giving tasks to teammates.

NVIDIA’s contests are “global developer contests”, but the contests are not open to developers in India and China. This is probably due to local rules and regulations governing how contests, prizes and taxes work. It is too bad; I would love to see what types of applications would come from participants in these countries.