import io
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image

app = FastAPI()

# Load model and processor
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct", torch_dtype="auto"
).to("cuda")
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")

class InferenceRequest(BaseModel):
    prompt: str

@app.post("/inference")
async def inference(image: UploadFile = File(...), prompt: str = Form(...)):
    try:
        # Read and process the uploaded image
        image_content = await image.read()
        pil_image = Image.open(io.BytesIO(image_content))

        # Prepare messages
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": pil_image},
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        # Prepare inputs for the model
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")

        # Generate output
        with torch.no_grad():
            generated_ids = model.generate(**inputs, max_new_tokens=128)

        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )

        return JSONResponse(content={"response": output_text[0]})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
