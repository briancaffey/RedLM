from tensorrt_llm import LLM, SamplingParams
from tensorrt_llm.hlapi import BuildConfig

TASK = "把下面的白话写成用简单的现代汉语的句子：\n"

prompts = [
    "此开卷第一回也。作者自云曾历过一番梦幻之后，故将真事隐去，而借“通灵”说此《石头记》一书也，故曰“甄士隐”云云。但书中所记何事何人？自己又云：今风尘碌碌，一事无成，忽念及当日所有之女子，一一细考较去，觉其行止见识皆出我之上，我堂堂须眉，诚不若彼裙钗。我实愧则有馀，悔又无益，大无可如何之日也！当此日，欲将已往所赖天恩祖德锦衣纨袴之时，饫甘餍肥之日，背父兄教育之恩，负师友规训之德，以致今日一技无成，半生潦倒之罪，编述一集，以告天下。知我之负罪固多，然闺阁中历历有人，万不可因我之不肖自护己短，一并使其泯灭也。所以蓬牖茅椽，绳床瓦灶，并不足妨我襟怀。况那晨风夕月，阶柳庭花，更觉得润人笔墨。我虽不学无文，又何妨用假语村言敷衍出来，亦可使闺阁昭传，复可破一时之闷，醒同人之目，不亦宜乎？故曰“贾雨村”云云。更于篇中间用“梦”“幻”等字，却是此书本旨，兼寓提醒阅者之意。",
    "宝钗等吃过点心，大家也有坐的，也有立的，也有在外观花的，也有倚栏看鱼的，各自取便，说笑不一。探春便和宝琴下棋，宝钗岫烟观局。黛玉和宝玉在一簇花下唧唧哝哝，不知说些什么。只见林之孝家的和一群女人，带了一个媳妇进来。那媳妇愁眉泪眼，也不敢进厅来，到阶下便朝上跪下磕头。探春因一块棋受了敌，算来算去，总得了两个眼，便折了官著儿，两眼只瞅著棋盘，一只手伸在盒内，只管抓棋子作想，－－林之孝家的站了半天－－因回头要茶时才看见，问什么事。",
]

prompts = [f"{TASK}\n{p}\n\n" for p in prompts]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=2048)
build_config = BuildConfig(max_seq_len=4096)


# Qwen/Qwen2-7B-Instruct
# baichuan-inc/Baichuan2-13B-Chat
llm = LLM(model="baichuan-inc/Baichuan2-13B-Chat", build_config=build_config)

outputs = llm.generate(prompts, sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
