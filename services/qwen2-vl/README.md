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

## Container

To build the container, log in to Docker Hub with `docker login`

Build the image and tag it:

```
$ docker build . -t briancaffey/qwen2-vl:latest
[+] Building 182.9s (11/11) FINISHED                                                                                                                             docker:default
 => [internal] load build definition from Dockerfile                                                                                                                       0.0s
 => => transferring dockerfile: 416B                                                                                                                                       0.0s
 => [internal] load metadata for docker.io/nvidia/cuda:12.1.1-base-ubuntu22.04                                                                                             0.2s
 => [internal] load .dockerignore                                                                                                                                          0.0s
 => => transferring context: 57B                                                                                                                                           0.0s
 => [1/6] FROM docker.io/nvidia/cuda:12.1.1-base-ubuntu22.04@sha256:457a4076c56025f51217bff647ca631c7880ad3dbf546b03728ba98297ebbc22                                       0.0s
 => [internal] load build context                                                                                                                                          0.0s
 => => transferring context: 631B                                                                                                                                          0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                                                              0.0s
 => CACHED [3/6] RUN apt-get update && apt-get install -y     git     python3.10     python3-pip                                                                           0.0s
 => [4/6] COPY requirements.txt ./                                                                                                                                         0.1s
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt                                                                                                             176.6s
 => [6/6] COPY . /app/                                                                                                                                                     0.1s
 => exporting to image                                                                                                                                                     5.8s
 => => exporting layers                                                                                                                                                    5.7s
 => => writing image sha256:c207439c8253a609019643d51a4bd333611441ac408266fb8c8bf9ab39fd4e8e                                                                               0.0s
 => => naming to docker.io/library/qwen2-vl:latest                                                                                                                         0.0s
```

Push the image to Docker Hub:

```
docker push briancaffey/qwen2-vl:latest
```

Run the container with `docker run`:

```
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    briancaffey/qwen2-vl:latest
```

Test the container with `python client.py --host localhost --port 8000`