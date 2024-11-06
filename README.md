# RedLM

![RedLM](/static/redlm/title.png)

## About

RedLM is an application for the study of Redology, or the study of one of China's greatest literary works: Dream of the Red Chamber. RedLM is built with software frameworks from NVIDIA and LlamaIndex and uses leading Chinese language models to perform Q&A based on both text and images. This application was developed for the NVIDIA and LlamaIndex Developer Contest.

### Submission Video

TODO: add twitter video link here

### Article Link

TODO: add briancaffey.github.io link here

## Running the application locally

The application is built with the following technologies:

- Backend API built with Python, FastAPI and LlamaIndex
- Frontend web UI built with Vue 3 and Nuxt 3
- Inference services (either using local services or NVIDIA Cloud APIs)

The application can run on Mac, Windows and Linux. Using local inference services requires Linux.

### Backend

There are three ways to run the backend application:

- virtual environment (Mac, Windows, Linux)
- docker (Linux recommended)
- Kubernetes (Linux required)

This README will cover instructions for running the backend API in a virtual environment on either Mac or Linux machines using the NVIDIA's Cloud APIs for inference. Docker and Kubernetes environment setup is documented separately:

- TODO: add docker documentation link
- TODO: add k8s documentation link


To get started with running the project in a virtual environment, copy the `redlm/.env.sample` file into a new file called `redlm/.env` and update the environment variables. To get started quickly, get an API key from `build.nvidia.com` and add it to `NVIDIA_API_KEY` in `redlm/.env`. For now, you can remove all other values from `redlm/.env`.

Create a virtual environment in `redlm`:

```bash
cd redlm
python3 -m venv .venv
source .venv/bin/activate
```

Next, build the VectorIndexStore with the following command (from inside the `redlm` directory):

```bash
python -m commands.index
```

This command will create a LlamaIndex VectorStoreIndex and save it to disk in the `redlm/storage` directory. You can view the generated index files with `ls storage`:

```
README.md
docstore.json
image__vector_store.json
default__vector_store.json
graph_store.json
index_store.json
```

The Milvus vector database can also be used with this project, see the section below about using `docker` for instructions on how to use Milvus.

Now you can start the FastAPI API server with the following command:

```
fastapi dev main.py --port 8080
```

### Frontend

The UI for RedLM is built with Vue 3 and Nuxt 3. It uses static assets (JSON files and PNG files) that live in the `redlm` directory, so you will need to create the following symbollic links:

```
ln -s $(pwd)/redlm/data/book $(pwd)/ui/public/
ln -s $(pwd)/redlm/data/paintings $(pwd)/ui/public/img/paintings
```

If this command does not work, you may need to manually copy the files over from `redlm/data` to the target directories:

```
redlm/data/book/{1,2,3}.json -> ui/public/book/{1,2,3}.json
redlm/data/paintings/{1,2,3}.png -> ui/public/img/paintings/{1,2,3}.png
```

To run the frontend application, run the following commands:

```
cd ui
yarn
yarn dev
```

Now you should be able to visit [localhost:3000](http://localhost:3000).

The frontend application has two main features: text-based Q&A and image-based Q&A.

Text-based Q&A will answer questions about the book using retrieval augmented generation (RAG) with LlamaIndex.

## Running services with docker

This project supports running services in docker with docker compose.

### `docker-compose.yml`

The `docker-compose.yml` file in the root of this project contains services for running the FastAPI server and the Nuxt UI app. Running `docker compose up` will start these services.

If you would like to use the Milvus vector database when running this project locally, you can use the docker compose file `services/milvus.docker-compose.yml` by running the following command from inside the `services` directory:

```
docker compose -f milvus.docker-compose.yml up
```

You will also need to configure the FastAPI service to use Milvus by setting the following value in the `redlm/.env` file:

```
USE_EXTERNAL_VECTORDB=True
```

Before running `docker compose up`, you can build the VectorIndexStore (or Milvus) embedding database with the command `docker compose run redlm-index`.

Image and JSON data are automatically mounted in the correct locations with volumes configured in the docker compose files, so they do not need to be copied if you are using docker compose.

Langfuse can be set up locally with docker compose by following instructions in the [Langfuse GitHub repository](https://github.com/langfuse/langfuse?tab=readme-ov-file#localhost-docker). Once you start Langfuse, you will need to create an organization, project, user and then create a credential. Then you will need to configure the following values in the `redlm/.env` configuration file:

```
LANGFUSE_SERVICE_HOST=localhost
LANGFUSE_SERVICE_PORT=3030
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
```

Note: the `LANGFUSE_SERVICE_PORT` value is different from the value used in the Langfuse docker-compose file (`3000`). Port `3000` is also used by Nuxt, so the Langfuse value will need to be something else since the Langfuse portal is exposed using this port on `localhost` (`3030`, for example).

Here is the output of `docker ps` with all of the services running locally (API server, UI, Langfuse and Milvus services):

```
CONTAINER ID   IMAGE                                      COMMAND                  CREATED         STATUS                  PORTS                              NAMES
7e802835da5c   redlm-redlm-ui                             "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes            0.0.0.0:3000->3000/tcp             redlm-ui
3444c41ad7c8   redlm-redlm-api                            "fastapi dev main.py…"   2 minutes ago   Up 2 minutes            0.0.0.0:8080->8000/tcp             redlm-api
6841cf64f8d7   langfuse/langfuse:2                        "dumb-init -- ./web/…"   30 hours ago    Up 30 hours             0.0.0.0:3030->3000/tcp             langfuse-langfuse-server-1
eb5bebfffadc   postgres                                   "docker-entrypoint.s…"   31 hours ago    Up 31 hours (healthy)   0.0.0.0:5432->5432/tcp             langfuse-db-1
ec984e68279d   milvusdb/milvus:v2.4.14                    "/tini -- milvus run…"   7 days ago      Up 7 days               0.0.0.0:19530->19530/tcp           milvus-standalone
0237aa66e8ae   quay.io/coreos/etcd:v3.5.0                 "etcd -advertise-cli…"   7 days ago      Up 7 days               0.0.0.0:2379->2379/tcp, 2380/tcp   milvus-etcd
0109b6349ea0   minio/minio:RELEASE.2020-12-03T00-03-10Z   "/usr/bin/docker-ent…"   7 days ago      Up 7 days (healthy)     9000/tcp                           milvus-minio
```

## Running Inferences services locally

Running inference services locally requires an NVIDIA GeForce RTX GPU. The following instructions assume the use of Ubuntu for the operating system. Everything here was tested on Ubuntu Desktop 24.04 LTS: Noble Numbat.

### Large Language Models

Large language models are used for doing inference with LlamaIndex. I primarily used the `01-ai/Yi-1.5-9B-Chat` model when developing the application on my PC. The easiest way to start this model is with vLLM's docker image. Before running this, make sure that you set your export your `HUGGING_FACE_HUB_TOKEN`. The following command also assumes that your Hugging Face cache uses the default location (`~/.cache/huggingface`):

```bash
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model 01-ai/Yi-1.5-9B-Chat --trust-remote-code
```

This model was a great all-purpose model to use for development of this project. I used it as the following:

- Q&A chatbot inference model used with LlamaIndex RAG system
- Translating from Chinese to English and from English to Chinese
- LLM for the Continue.dev VSCode plugin used for simple questions while writing code

You can read more about the `01-ai/Yi` model series on [their GitHub repo](https://github.com/01-ai/Yi?tab=readme-ov-file#introduction).

### (small) Vision Language Models

I wrote a simple FastAPI service based on the `Qwen/Qwen2-VL-2B-Instruct` quickstart example [here](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct#quickstart) using Claude 3.5 Sonnet. Most of the code for this project was written with Claude 3.5 Sonnet (using their generous free plan!)

TODO: Since I wrote this service, Qwen2.5 models have been released, update this service to use the Qwen2.5 models.

Instructions for starting this service can be found under [`services/qwen2-vl/README.md`](services/qwen2-vl/README.md). This also uses FastAPI, and the command to start it is:

```
fastapi dev main.py --host 0.0.0.0 --port 8000
```

The Qwen2-VL model can also be started with docker. I use a custom docker image based on an `nvidia/cuda` base image:

```
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    briancaffey/qwen2-vl:latest
```
