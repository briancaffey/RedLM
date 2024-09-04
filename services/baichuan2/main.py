from typing import List, Dict
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

class ChatCompletionRequest(BaseModel):
    messages: List[Dict[str, str]]

class ChatCompletionResponse(BaseModel):
    choices: List[Dict[str, str]]

app = FastAPI()
MODEL = "baichuan-inc/Baichuan2-7B-Chat"
# Load the pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL, use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained(MODEL)

# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from transformers.generation.utils import GenerationConfig
# tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", use_fast=False, trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
# model.generation_config = GenerationConfig.from_pretrained("baichuan-inc/Baichuan2-7B-Chat")
# messages = []
# messages.append({"role": "user", "content": "解释一下“温故而知新”"})
# response = model.chat(tokenizer, messages)
# print(response)

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completion(request: ChatCompletionRequest):
    messages = request.messages
    if not messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    response = model.chat(tokenizer, messages)

    return {"choices": [{"message": {"content": response}}]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
