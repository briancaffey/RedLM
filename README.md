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
- Milvus vector database (optional)
- Langfuse for observability (optional)

The application can run on Mac, Windows and Linux. Using local inference services requires Linux.

### Backend

There are two ways to run the backend application:

- virtual environment (tested on Mac and Linux; should work on WSL)
- docker (test on Mac and Linux; should work on WSL )

To get started, copy the `redlm/.env.sample` file into a new file called `redlm/.env`. Obtain an API key from [`build.nvidia.com`](https://build.nvidia.com) and add it to `NVIDIA_API_KEY` in `redlm/.env`. Also be sure to configure `LLM_NAME`, `COMPLETION_MODEL`, `VLM_MODEL_NAME` and `VLM_INVOKE_URL`. These can all use the default values found in the `redlm/.env.sample` file. These values can be changed to use different models available in NVIDIA's API catalog. Configuring local LLMs running on RTX workstations is covered at the end of this README file.

Create a virtual environment in the `redlm` directory:

```bash
cd redlm
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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

The UI for RedLM is built with Vue 3 and Nuxt 3. It uses static assets (JSON files and PNG files) that live in the `redlm` directory, so you will need to create the following symbolic links:

```
ln -s $(pwd)/redlm/data/book $(pwd)/ui/public/
ln -s $(pwd)/redlm/data/paintings $(pwd)/ui/public/img/paintings
```

If this command does not work, you may need to manually copy the files over from `redlm/data` to the target directories. The files should be copied as follows:

```
redlm/data/book/{1,2,3}.json -> ui/public/book/{1,2,3}.json
redlm/data/paintings/{1,2,3}.png -> ui/public/img/paintings/{1,2,3}.png
```

To run the frontend application, run the following commands (it is recommended to use Node v20.18.0 and yarn 1.22.22):

```
cd ui
yarn
yarn dev
```

Now you should be able to visit [localhost:3000](http://localhost:3000).

## Features

![RedLM Homepage](/static/redlm/homepage.png)

This home page lists all of the chapters. Click on a chapter and view it.

![RedLM chapter page](/static/redlm/chapterpage.png)

The chapter page displays all of the chapter's associated images at the top of the page, and the text and translation is displayed below.

- The left column is the original text
- The center column is the original text rewritten in simple, modern Mandarin
- The right column is a translation of the simple, Modern Mandarin into English

Click on one of the smaller images at the top of the page to ask a question about the painting.

![RedLM Image Q&A](/static/redlm/image_qa_example.png)

Click and drag on a portion of the image and then enter a query in the text box below about that part of the image. The response is displayed in the red text box, and references used by Retrieval Augmented Generation system can be viewed by hovering over the green badges below the response. Hovering over the gray badge will display the original description of the image based on your question (without using reference material from the book). The response (in the red dialog box) incorporates the referenced passages and the image description in a custom prompt and attempts to explain the content of the image in the context of the image's associated chapter. This means that only paragraphs from the painting's associated chapter will be used to generate the response.

This diagram shows the overall flow of data in the image Q&A bot.

![Image Q&A Diagram](/static/redlm/redlm.drawio.png)

1. The user selects part of an image and writes a question. This data is then sent to the RedLM API as a post request to the `/mm-q-and-a` endpoint (multi-modal Q&A).
2. Vision language models are used to get a description of the image. Depending on the application configuration, this query can use models such as `Qwen/Qwen2-VL-2B-Instruct` on RTX PCs or using the NVIDIA API Catalog using larger models such as `meta/llama-3.2-90b-vision-instruct`. Not all vision language models have the same interface, so I added some logic to handle different model formats.
3. The image description is used to fetch relevant documents from the Vector Database
4. The full prompt with the image description and relevant documents is sent to the LLM. Again, inference for this step is done either with RTX PCs or using models from the `build.nvidia.com` API catalog.
5. The response from the LLM is sent back to the browser and is displayed to the user as a chat message.

The Q&A tab in the navigation menu allows for asking questions about the entire book.

![Text Q&A example](/static/redlm/qa_example_flower_pedals_a.png)

The image Q&A bot and the text Q&A bot support answer questions in both Chinese and English.

## Running services with docker

This project supports running services in docker with docker compose.

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
