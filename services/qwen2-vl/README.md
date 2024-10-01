# Qwen2-VL

Qwen2-VL is a new multi-modal LLM that can understand images. This service provides a simple FastAPI server for processing requests with images.

Image content is described by Qwen2-VL, and results are used to make RAG queries. The goal is to be able to add contextual data from the book that is related to a given image.

For example, if the image contains people playing a board game, then the query may include a specific paragraph about people playing a board game.

## Install dependencies

```
cd services/qwen2-vl
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start the service

```
fastapi dev main.py --host 0.0.0.0 --port 8000
```
