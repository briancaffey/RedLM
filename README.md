# RedLLM

## Docker commands for LLMs

```
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model 01-ai/Yi-1.5-6B-Chat --trust-remote-code
```

```
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model 01-ai/Yi-1.5-9B-Chat --trust-remote-code
```


## Example of RAG Answer a question correctly where LLM alone gets the question wrong

荣两处上下内外人等莫不欢天喜地，独有宝玉置若罔闻。你道什么缘故？原来近日水月庵的智能私逃入城，来找秦钟，不意被秦邦业知觉，将智能逐出，将秦钟打了一顿，自己气的老病发了，三五日便呜呼哀哉了。秦钟本自怯弱，又带病未痊，受了笞杖，今见老父气死，悔痛无及，又添了许多病症。因此，宝玉心中怅怅不乐。虽有元春晋封之事，那解得他的愁闷？贾母等如何谢恩，如何回家，亲友如何来庆贺，宁荣两府近日如何热闹，众人如何得意，独他一个皆视有如无，毫不介意。因此，众人嘲他越发呆了。

Mandarin:

荣府和宁府的上下内外所有人都非常高兴，唯独宝玉对此毫不在意。你想知道是什么原因吗？原来，最近水月庵的尼姑智能私自逃进城里找秦钟，没想到被秦钟的父亲秦邦业发现了。秦邦业不仅把智能赶走，还打了秦钟一顿，自己也因此气得旧病复发，过了三五天便去世了。秦钟本来身体就虚弱，之前还生病未愈，如今又挨了打，看到父亲因为生气而去世，后悔痛苦不已，病情更严重了。因此，宝玉心里感到非常郁闷。虽然元春晋升为贵妃是件喜事，但这并不能解开他心中的烦忧。贾母等人忙着谢恩回府，亲友们纷纷前来庆贺，宁荣两府最近十分热闹，众人也都得意非常，唯有宝玉对这一切都毫不在意，完全不放在心上。因此，大家都笑话他越来越呆滞了。

English

Everyone in the Rong and Ning households, both inside and outside, were extremely happy, except for Baoyu, who seemed indifferent. Do you want to know why? It turns out that recently, the nun Zhineng from Shuiyue Temple secretly ran into the city to find Qin Zhong. Unexpectedly, she was discovered by Qin Zhong's father, Qin Banger. Qin Banger not only drove Zhineng away but also gave Qin Zhong a beating. This made Qin Banger so angry that his old illness relapsed, and within three to five days, he passed away. Qin Zhong had always been weak and hadn't fully recovered from a previous illness. After being beaten and seeing his father die in anger, he was overwhelmed with regret and sorrow, which worsened his condition. As a result, Baoyu felt very melancholic. Although the promotion of Yuan Chun to imperial concubine was a joyful event, it couldn't alleviate the gloom in his heart. While Grandmother Jia and others were busy expressing their gratitude and returning home, and relatives and friends came to celebrate, and the Rong and Ning households were bustling with excitement, Baoyu alone remained completely indifferent to it all. Consequently, everyone started to mock him for becoming more and more absent-minded.



```json
"question": "秦钟的父亲是如何死的？[1分]",
"choices": [
    [
        "A",
        "外感风寒、风毒之症"
    ],
    [
        "B",
        "被智能儿气死的"
    ],
    [
        "C",
        "生气引发旧病加重"
    ],
    [
        "D",
        "生气而诱发中风而死"
    ]
],
```