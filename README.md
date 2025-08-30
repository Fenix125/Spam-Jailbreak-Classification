![Logo of the project](app/frontend/src/assets/robot_classifier_img_2.png)

# Spam/Jailbreak Classification

## Description

> This project was created during a two‑month ML/Python Summer Camp at **[Unidatalab](https://unidatalab.com)**.
> Thanks to the company for the provided opportunity. Also I would like to give credit to
> my mentor **[Maksym Komar](https://www.linkedin.com/in/maksym-komar/)** for his support and guidance throughout this journey.

Spam/Jailbreak Classification project shows the gained knowledge of Machine Learning applied to practice
It was made in 3 steps:

### Step 1. Fine-Tuning a Base BERT Model

Here a [BERT Model](https://huggingface.co/google-bert/bert-base-uncased) was fine-tuned using [transformers](https://huggingface.co/docs/transformers/index) on a previously filtered dataset.
The dataset consists of two merged datasets:

-   [190K+ Spam | Ham Email Dataset for Classification](https://www.kaggle.com/datasets/meruvulikith/190k-spam-ham-email-dataset-for-classification)
-   [Emails for spam or ham classification (Trec 2007)](https://www.kaggle.com/datasets/bayes2003/emails-for-spam-or-ham-classification-trec-2007)

The data preprocessing included removal of duplicate and null values. The merged dataset was splitted into:

-   Training set (72%)
-   Validation set (18%)
-   Test set (10%)

### Step 2. Wrapping the Fine-Tuned Model into an Agentic pipeline

Here the [LangChain](https://www.langchain.com) framework was used to build an agent with two tools:

1. **classify_spam_ham** tool uses the trained bert model predict whether a text is spam or ham, returns result to agent
2. **search_info_about_Mykhailo_Ivasiuk** this is a RAG tool that retrieves my biography information from the provided document

The agent has memory, which helps him remember previous conversations.

The LangChain agent is also accessible as a terminal application

### Step 3. Software implementation

Here the [FastAPI](https://fastapi.tiangolo.com) framework was used to create a microservice architecture with 3 endpoints:

-   /api/agent: uses LangChain agent
-   /api/spam_ham_classifier: uses the spam/ham classifier to classify text
-   /api/bio_search: returns relevant information about student's biography (mine)

Also the /external/mcp endpoint is available for mcp tools

The [React](https://react.dev) library for web and native user interfaces was used for minimalistic user interface

Also there exists an telegram chatbot which uses the FastAPI server to make requests to /api/agent endpoint

The [Gradio](https://www.gradio.app) open-source Python package was used to deliver a demo application that will be available to other users

## Installing / Getting started

The easiest way to run the project locally is via the provided Makefile or docker-compose.yml.

> [!IMPORTANT]
> You will need Python and Node JS (for the front‑end) if not using Docker.

### Initial Configuration

> [!WARNING]
> You will need to set up envoronment variables in order for the project to work locally

The .env.example file shows the required variables, including:

-   OPENAI_API_KEY: API key of [OpenAI developer platform](https://platform.openai.com/docs/overview), used for access to open ai models
-   OPENAI_MODEL: Chat model name (**default**: gpt-4o-mini)
-   CLASSIFIER_MODEL: HuggingFace path for classifier model (**default:**: my pretrained spam-ham-classifier)
-   EMBED_MODEL: Name of the OpenAI embedding model used for RAG (**default**: text-embedding-ada-002)
-   FILE_PATH: Path to the text corpus (**default**: data/student_bio.txt)
-   APP_BACKEND_HOST/APP_BACKEND_PORT: Network address for the backend server, you can keep the by default
-   APP_FRONTEND_HOST/APP_FRONTEND_PORT: Network address for the React front‑end, you can keep the by default
-   RUN_MODE: Set to web (default) to start the HTTP server or cli to run in the command line
-   TELEGRAM_BOT_TOKEN: Token for the Telegram bot (optional)

### Clone the repository

```shell
git clone https://github.com/Fenix125/Spam-Jailbreak-Classification.git
cd Spam-Jailbreak-Classification
```

### Makefile

Use the Makefile to create a virtual environment, install Python requirements and fetch front‑end packages.
This also ensures a .env file exists

```shell
make install
```

**_Other useful commands:_**

```shell
make backend #starts FastAPI backend server
make frontend #starts React frontend server
make cli #starts terminal application
make bot #starts telegram bot
make gradio #runs web demo using Gradio
```

### Docker

```shell
docker compose up -d --build  #builds the images, created and starts compose stack
```

**_tips:_**

```shell
docker compose stop #stop running containers
docker compose start #used to restart containers that were previously created and are currently in a stopped state

docker compose down #stops and removes containers
docker compose up #build, create and start containers
```

## Developing

To develop the project further, clone the repository and install dependencies as shown above. The Python code lives in `app/backend` and is organised into agents, services, base classes and settings. The React code resides in app/frontend. You can modify the agent or add new tools in `app/backend/agent/tools.py`; the front‑end can be customised in `app/frontend/src`. The back‑end can be restarted by stopping and re‑running `make backend`.

## Features

-   Chat agent - built with LangChain and OpenAI’s models that routes your query to either the classifier or the RAG tool
    -   Message classification - send any piece of text and receive a label of spam or ham
    -   Retrieval‑augmented answering – ask a question about the biography of Mykhailo Ivasiuk and get the most
        relevant info from the corpus
-   Multiple interfaces - interact via a browser, command‑line, Telegram bot or Gradio demo
-   Containerized deployment - ready to run with Docker Compose; mounts the data folder into the backend

## Links

1.  Repository: https://github.com/Fenix125/Spam-Jailbreak-Classification
2.  Datasets:

    -   [190K+ Spam | Ham Email Dataset for Classification](https://www.kaggle.com/datasets/meruvulikith/190k-spam-ham-email-dataset-for-classification)

    -   [Emails for spam or ham classification (Trec 2007)](https://www.kaggle.com/datasets/bayes2003/emails-for-spam-or-ham-classification-trec-2007)

3.  Frameworks/Libraries:
    -   [Transformers](https://huggingface.co/docs/transformers/index)
    -   [LangChain](https://www.langchain.com)
    -   [FastAPI](https://fastapi.tiangolo.com)
    -   [React](https://react.dev)
    -   [Gradio](https://www.gradio.app)

## Licensing

"The code in this project is licensed under the Apache License 2.0. See LICENSE.
This distribution also includes a NOTICE file with attribution information."
