# Changelog

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
