# Changelog

## [0.10.0](https://github.com/briancaffey/RedLM/compare/v0.9.0...v0.10.0) (2024-11-09)


### Features

* **article:** add section about redlm deep dive video ([5ed0c85](https://github.com/briancaffey/RedLM/commit/5ed0c8569985405c428d4754b1b5c3bb86f3a8c6))
* **article:** expand section about llamaindex and add paragraph on LLMRerank ([7dac701](https://github.com/briancaffey/RedLM/commit/7dac70155ffccbaa128c768416d7ff318c644792))
* **article:** reword article, add links ([03384f0](https://github.com/briancaffey/RedLM/commit/03384f00b5c96d1b2c0d0dec1bd9a5e1227c8bc3))
* **docker:** update docker and docker compose configuration and documentation in readme ([5c6c80e](https://github.com/briancaffey/RedLM/commit/5c6c80e473e7a64cedb99a43e34d775151b53163))
* **nginx:** add nginx config for running api and ui on same domain ([9af720c](https://github.com/briancaffey/RedLM/commit/9af720c5b36a33358bd35df49773c8941573d0ea))
* **rag:** rector CustomQueryEngine, add observability with langfuse, fix issues with PromptTemplates and RAG logic ([0133cd3](https://github.com/briancaffey/RedLM/commit/0133cd389dc5a669fb78fdc3444a4b387e31264f))
* **readme:** update readme instructions and add section about redlm features ([0a3d072](https://github.com/briancaffey/RedLM/commit/0a3d072906128268ac5cd109e8e42b3f6b421a06))
* **workflow:** fully integrate llama-indeex workflows into FastAPI application ([5003174](https://github.com/briancaffey/RedLM/commit/50031747378cb8aa6ed632ca201cfb1fce95c199))
* **workflows:** add workflow for rag Q&A bot using rerank ([bccd6e6](https://github.com/briancaffey/RedLM/commit/bccd6e6221ccd2d3932165470965544c06a5ebff))


### Bug Fixes

* **black:** format code with black ([a7c7b35](https://github.com/briancaffey/RedLM/commit/a7c7b35fd31458d6c87254ef93f2a789eb0d6b56))
* **typo:** fix typo in logging ([1e5427b](https://github.com/briancaffey/RedLM/commit/1e5427b1ece1fbd299b437684e16b4d52aa4ef45))
* **workflows:** filter index by chapter when processing image Q&A requests ([9182f3b](https://github.com/briancaffey/RedLM/commit/9182f3bfb66481171bc000769c1103b165bf5943))

## [0.9.0](https://github.com/briancaffey/RedLM/compare/v0.8.0...v0.9.0) (2024-11-04)


### Features

* **article:** add section about models used in RedLM ([bff2f70](https://github.com/briancaffey/RedLM/commit/bff2f70132e408a124f6e01d466286cc689af589))
* **article:** draft of final thoughts ([fa9d13f](https://github.com/briancaffey/RedLM/commit/fa9d13f5018f6320162b0fae741513374a9685a0))
* **article:** update article with more examples ([b92215e](https://github.com/briancaffey/RedLM/commit/b92215e34a331051ce6a7a92447b9aee6fd16c60))
* **article:** update article with more examples and images ([ef96491](https://github.com/briancaffey/RedLM/commit/ef964912ace038cef330a9669e4dfe021d423024))
* **index:** use both english and chinese embed models during indexing ([25c4135](https://github.com/briancaffey/RedLM/commit/25c413589888c5405a72be1dd566c1ce76ff3499))
* **index:** use both english and chinese embed models during indexing ([cab16ec](https://github.com/briancaffey/RedLM/commit/cab16ec0ec94329b577ae90e6630fd82d3bc619a))
* **language:** support for Q&A queries in English and Chinese with dynamic prompts, update article, add examples ([780b5a7](https://github.com/briancaffey/RedLM/commit/780b5a7dcd102450e6844fa2937d161dc015d9fe))
* **milvus:** add support for using external milvus server with docker compose via env var configuration ([872a2b0](https://github.com/briancaffey/RedLM/commit/872a2b040ddb04ba0d805710cbe084d437397348))


### Bug Fixes

* **typo:** fix all typos in article using spellcheck extension cSpell ([3f151c0](https://github.com/briancaffey/RedLM/commit/3f151c0367436676d2a25d67d77d17ef3a2e8261))
* **ui:** fix issue with cn function from shadcn and radix ([ce11c5d](https://github.com/briancaffey/RedLM/commit/ce11c5d523133343bfba09b811b50e7dc8e2e570))

## [0.8.0](https://github.com/briancaffey/RedLM/compare/v0.7.0...v0.8.0) (2024-10-22)


### Features

* **article:** add article complete rough draft in markdown format with images ([c3741df](https://github.com/briancaffey/RedLM/commit/c3741dfe30cdcd7b010decf706cb789e26e6aec9))
* **article:** rtx pc cluster, tailscale, notebooklm, cloudflare tunnels ([c4af786](https://github.com/briancaffey/RedLM/commit/c4af786883c04edf79c2686f13a9f10a8adc10c9))
* **k8s:** add qwen2-vl service kubernetes config using kustomize ([738afd3](https://github.com/briancaffey/RedLM/commit/738afd3a03961ec2fdef45058e6c0a08cc52cefb))
* **kustomize:** add llm service to kustomize configuration ([ff84540](https://github.com/briancaffey/RedLM/commit/ff84540949b2af2b72b88387a39d5711d2b832d0))

## [0.7.0](https://github.com/briancaffey/RedLM/compare/v0.6.0...v0.7.0) (2024-10-05)


### Features

* **article:** add initial draft of article and images ([3413882](https://github.com/briancaffey/RedLM/commit/34138825f052509442daa9e30044bff0bca5d108))
* **docker:** add docker config config for ui app ([0585afd](https://github.com/briancaffey/RedLM/commit/0585afd337cef6bb3b979a22dd706c8c83f9fdd9))
* **docker:** add docker config for redlm-api fastapi backend ([cc0ac00](https://github.com/briancaffey/RedLM/commit/cc0ac006c61f635ea3cb58af7a139c44da3b77a6))
* **docs:** update readme with instructions on how to start inferences services locally for llm and vlm ([cab78c6](https://github.com/briancaffey/RedLM/commit/cab78c6c3d208480dba30254d2f73d0d63f5768d))


### Bug Fixes

* **llm:** add max_tokens to local llm config and LLM_NAME env var ([063d2ae](https://github.com/briancaffey/RedLM/commit/063d2ae26be0593f4e00457c929e5f43c59351d6))

## [0.6.0](https://github.com/briancaffey/RedLM/compare/v0.5.0...v0.6.0) (2024-10-01)


### Features

* **data:** add json files with chapter data, text and translations ([854a619](https://github.com/briancaffey/RedLM/commit/854a6196f85392df548e13756d72f7bca0451ac3))
* **name:** rename hllm directory to redlm ([2d3f662](https://github.com/briancaffey/RedLM/commit/2d3f662cbc5bc5201191d81365853c8d3771878b))


### Bug Fixes

* **git:** add .gitkeep to ui/public/img to keep folder ([dd9e1b8](https://github.com/briancaffey/RedLM/commit/dd9e1b8e043c3a50cddbdca4bb778ec40ef766d2))
* **git:** add .gitkeep to ui/public/img to keep folder ([74367b1](https://github.com/briancaffey/RedLM/commit/74367b1aa7d9042ea69f9a2167c6eadc44906beb))

## [0.5.0](https://github.com/briancaffey/HLLM/compare/v0.4.0...v0.5.0) (2024-09-30)


### Features

* **evaluation:** update logging in scripts for evaluation ([e6e9606](https://github.com/briancaffey/HLLM/commit/e6e96066217441421b8c9dabfb9c23c8dafaca6f))
* **multi-modal-rag:** finish implementation of multi-modal rag ([c38a356](https://github.com/briancaffey/HLLM/commit/c38a356902fc82a3942ab1b8e05a530834a5e969))
* **nims:** use NIMs for LLM inference ([53b49ab](https://github.com/briancaffey/HLLM/commit/53b49abc990e5488a7fe78f14d59a51b1d409ca4))
* **nvidia:** finish implementation of nvidia cloud apis for image q&a with vision language models ([f8ff0b3](https://github.com/briancaffey/HLLM/commit/f8ff0b3a4c45b23045f6ff6acfc318e244715e13))
* **translation:** improve logging for translation script ([7aa55b4](https://github.com/briancaffey/HLLM/commit/7aa55b48ea28fb44fea03c55137c4f17b016d496))
* **translation:** translated all 120 chapters successfully, fixed context window errors, tuned LLM parameters ([fb05ed5](https://github.com/briancaffey/HLLM/commit/fb05ed5c4bcf0946d5df34c3edf9ccb050eaa048))
* **translation:** update script for translation ([aad58dd](https://github.com/briancaffey/HLLM/commit/aad58dd1533dd2d523218528211ed03d280d8bff))
* **translation:** update translation script and translation prompts, add new translation using Qwen2-7B base model ([6978bd4](https://github.com/briancaffey/HLLM/commit/6978bd46d7338003bfcf62666bf7f911b61f7784))
* **ui:** better styles for reference badges and image selection ([8934f5e](https://github.com/briancaffey/HLLM/commit/8934f5e098992361d50c2514e18ffcdbca1c9ed9))


### Bug Fixes

* **lint:** format code with black ([12b1835](https://github.com/briancaffey/HLLM/commit/12b183568bd8939144919ea884cd0dcb5be3bb28))
* **ui:** formatting for mmqa ui ([49d012a](https://github.com/briancaffey/HLLM/commit/49d012a9e0d6bca84e3b9d11469f86f28c19d203))

## [0.4.0](https://github.com/briancaffey/HLLM/compare/v0.3.0...v0.4.0) (2024-09-12)


### Features

* **metadata:** return node metadata from query engine and display in ui ([ff7eab3](https://github.com/briancaffey/HLLM/commit/ff7eab3d536350d26f06cb3f9faab4752fe044ff))
* **multi-gpu:** changes to support distributed LLM generation ([296e774](https://github.com/briancaffey/HLLM/commit/296e774c6c3964261b711d993700e570a656f185))
* **multi-modal-ui:** add formatting to image chat form and text boxes ([b22390b](https://github.com/briancaffey/HLLM/commit/b22390bbd9062d5f51a0f89228080736fdd04b5c))
* **multi-modal:** add endpoint and test script for multi-modal Q and A ([87baeb7](https://github.com/briancaffey/HLLM/commit/87baeb7224e33608a07e4669e838f7d870655ed5))
* **multi-modal:** add pinia store for multi-modal data and refactor image page to use script setup syntax ([96e4dea](https://github.com/briancaffey/HLLM/commit/96e4dea27af541bc9dafa9d584c2d1c474f50bc6))
* **q-and-a-ui:** improve formatting for q and a component, fix navigation errors ([a0807d9](https://github.com/briancaffey/HLLM/commit/a0807d96f8249ef3bdf1c29f9024eed64157db8e))
* **rag:** add additional endpoint for question and answer ([63aab04](https://github.com/briancaffey/HLLM/commit/63aab04c42b05288d63d36c503fb63259ae790e3))
* **translation:** add mandarin and english translations to chapter detail page ([00b9b0a](https://github.com/briancaffey/HLLM/commit/00b9b0a7a3474d5bde73557ea2e5d89c40abaf2e))
* **translation:** add translations made with qwen2-7b-chat ([5051deb](https://github.com/briancaffey/HLLM/commit/5051deb56a7aa65dfd32b64bc6faba8f8acbd468))
* **translations:** add additional translations using qwen2-7b-chat ([d29b51a](https://github.com/briancaffey/HLLM/commit/d29b51a8f800cacf3f24d8e7d24b84f0779e5265))
* **trt-llm-api:** use tensorrt-llm api to do translation, add sample translation for chapter 111 ([3cca5b6](https://github.com/briancaffey/HLLM/commit/3cca5b6077cdfc5a62bc96d0048d9b644db5fbb8))
* **ui:** add modified drawer component for displaying chat message responses ([befa2b0](https://github.com/briancaffey/HLLM/commit/befa2b095f5c4e1b29512d4a94e28662f4db9989))
* **ui:** fix fastapi and ui integration issues, add Q and A page ([51d4acb](https://github.com/briancaffey/HLLM/commit/51d4acbb4b3c023ea6927f5cbe2077505da29161))


### Bug Fixes

* **lint:** format with black ([991664b](https://github.com/briancaffey/HLLM/commit/991664b05cef300a1ecb6ecb482fc2a59d3de11e))
* **ui:** scroll to bottom after question is answered ([833a45a](https://github.com/briancaffey/HLLM/commit/833a45af9a2895b6b01b10a1fb0aa5ffab5dbec0))

## [0.3.0](https://github.com/briancaffey/HLLM/compare/v0.2.0...v0.3.0) (2024-09-08)


### Features

* **black:** format code with black ([39c1342](https://github.com/briancaffey/HLLM/commit/39c1342ca58eedf31d80c1f48453dac11d6e2164))
* **index:** refactor RAG server, add command to build and persist VectorIndexStore data ([62405f9](https://github.com/briancaffey/HLLM/commit/62405f94c809d1493b8be4cb78a24a023f04f431))


### Bug Fixes

* **black:** format with black ([90725e1](https://github.com/briancaffey/HLLM/commit/90725e110cd1fc4557543eee67d7652ed511a9ee))

## [0.2.0](https://github.com/briancaffey/HLLM/compare/v0.1.0...v0.2.0) (2024-09-07)


### Features

* **img:** rename images ([dbb7cbe](https://github.com/briancaffey/HLLM/commit/dbb7cbe7c3996e3adc60cef8bf498f63564b2fb9))
* **ui:** add pinia for chapter store, add components on index page ([c4975ed](https://github.com/briancaffey/HLLM/commit/c4975ed3ea510245ed2aff61073865339e26d6fe))
* **ui:** updates to UI for reading text and viewing images ([10ddabe](https://github.com/briancaffey/HLLM/commit/10ddabe39c749671e453888f30c365da67e38d3a))

## 0.1.0 (2024-09-07)


### Features

* **baichuan:** add service for baichuan2 ([be077f4](https://github.com/briancaffey/HLLM/commit/be077f424aad6bcaa8650dc3237cc55f5774b0a7))
* **eval:** improve evalution scripts and optimize prompts for better eval score ([f754c88](https://github.com/briancaffey/HLLM/commit/f754c8885bf05fb7ccf2cae85194c3eb0fca6157))
* **img:** add scaled down images of paintings ([0066b55](https://github.com/briancaffey/HLLM/commit/0066b55b896364fc9a0e58666494d5d21b24050e))
* **python:** python env ([3e43f4f](https://github.com/briancaffey/HLLM/commit/3e43f4fcde5898c0bc6b3e0e6ec60e17392352cf))
* **qwen2-vl:** add qwen2-vl service for multimodal LLM ([769d387](https://github.com/briancaffey/HLLM/commit/769d387c2a84c370ae2f37566fc2311fa8fccc2b))
* **qwen2-vl:** fixes for qwen2-vl service, example client API call now working ([8f5af85](https://github.com/briancaffey/HLLM/commit/8f5af852ad9d0cd60edec7ea081ad8c2b0e4c061))
* **rag:** add basic rag example in a sample script ([c9c7efa](https://github.com/briancaffey/HLLM/commit/c9c7efa44f41f351d22c23d7bbf658da3b92f47c))
* **rag:** add fastapi server for serving llama index rag app ([b2e72ac](https://github.com/briancaffey/HLLM/commit/b2e72ac2be8c9dca615219f4347e4cd2a17c6a7c))
* **release:** add release please for changelog ([7713e90](https://github.com/briancaffey/HLLM/commit/7713e909d04a19b3afa8e01739414e6bb8e86c9b))
* **scripts:** add scripts for text processing, evaluation, components for displaying text and cropping images ([df273ba](https://github.com/briancaffey/HLLM/commit/df273bab7b34728ccdc94a1af2b4ca5846c77a29))
* **text:** add text and scraping script ([eb8dc55](https://github.com/briancaffey/HLLM/commit/eb8dc552ee1fcdc001fbe9d5765e18afafce0423))
* **ui:** add basic ui with nuxt ([93da4c1](https://github.com/briancaffey/HLLM/commit/93da4c13733ed1d7a65c6286bc9311884751ec8e))
* **vue:** add shadcn helper functions and component code ([dfe04db](https://github.com/briancaffey/HLLM/commit/dfe04db1d1bf0def0af2a4ef08cc12a898eeaad3))
