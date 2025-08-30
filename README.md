![Logo of the project](app/frontend/src/assets/robot_classifier_img_2.png)

# Spam/Jailbreak Classification

## Description

> This project was created during a two‑month ML/Python Summer Camp at **[Unidatalab](https://unidatalab.com)**.
> Thanks to the company for the provided opportunity. I would also like to give credit to
> my mentor **[Maksym Komar](https://www.linkedin.com/in/maksym-komar/)** for his support and guidance throughout this journey.

The Spam/Jailbreak Classification project demonstrates the application of Machine Learning to practice.

It was completed in three major steps:

### Step 1. Fine-Tuning a Base BERT Model

In this step, a [BERT Model](https://huggingface.co/google-bert/bert-base-uncased) was fine-tuned using [transformers](https://huggingface.co/docs/transformers/index) on a preprocessed dataset.

The dataset is a combination of two datasets:

-   [190K+ Spam | Ham Email Dataset for Classification](https://www.kaggle.com/datasets/meruvulikith/190k-spam-ham-email-dataset-for-classification)
-   [Emails for spam or ham classification (Trec 2007)](https://www.kaggle.com/datasets/bayes2003/emails-for-spam-or-ham-classification-trec-2007)

Preprocessing steps included the removal of duplicate and null values. The merged dataset was then split into:

-   Training set (72%)
-   Validation set (18%)
-   Test set (10%)

### Step 2. Wrapping the Fine-Tuned Model into an Agentic pipeline

Using the [LangChain](https://www.langchain.com) framework, I built an agent with two tools:

1. **`classify_spam_ham`**: a tool that uses the trained BERT model to classify text as spam or ham.
2. **`search_info_about_Mykhailo_Ivasiuk`**: a Retrieval-Augmented Generation (RAG) tool that retrieves biographical information about Mykhailo Ivasiuk from a provided document.

The agent also has memory, allowing it to remember previous conversations. Moreover it is accessible as a terminal application.

### Step 3. Software implementation

I used the [FastAPI](https://fastapi.tiangolo.com) framework to create a microservice architecture with the following endpoints:

-   **`/api/agent`**: uses the LangChain agent
-   **`/api/spam_ham_classifier`**: uses the spam/ham classifier to classify text
-   **`/api/bio_search`**: returns relevant information about Mykhailo Ivasiuk's biography.

Additionally, there is an **`/external/mcp`** endpoint available for MCP tools.

For the frontend I used the [React](https://react.dev) library to build a minimalistic user interface

A Telegram chatbot is also available, which interacts with the FastAPI server by making requests to the **`/api/agent`** endpoint.

The [Gradio](https://www.gradio.app) package is used to provide a demo application for the project.

## Installing / Getting started

The easiest way to run the project locally is via the provided Makefile or docker-compose.yml.

> [!IMPORTANT]
> You will need Python and Node JS (for the front‑end) if not using Docker.
> Also make sure to set up envoronment variables in order for the project to work.

### Initial Configuration

The `.env.example` file shows the required variables, including:

-   `OPENAI_API_KEY`: a key from [OpenAI developer platform](https://platform.openai.com/docs/overview) used to access OpenAI models.
-   `OPENAI_MODEL`: Chat model name (**default**: `gpt-4o-mini`)
-   `CLASSIFIER_MODEL`: HuggingFace path for the classifier model (**default:**: my pretrained `spam-ham-classifier`)
-   `EMBED_MODEL`: Name of the OpenAI embedding model used for RAG (**default**: `text-embedding-ada-002`)
-   `FILE_PATH`: Path to the text corpus (**default**: `data/student_bio.txt`)
-   `APP_BACKEND_HOST/APP_BACKEND_PORT`: Network address for the backend server, you can keep them by default
-   `APP_FRONTEND_HOST/APP_FRONTEND_PORT`: Network address for the React front‑end, you can keep them by default
-   `RUN_MODE`: Set to `web`(default) to start the HTTP server or `cli` to run in the command line
-   `TELEGRAM_BOT_TOKEN`: Token for the Telegram bot (optional)

### Clone the repository

```shell
git clone https://github.com/Fenix125/Spam-Jailbreak-Classification.git
cd Spam-Jailbreak-Classification
```

### Makefile

Use the **Makefile** to create a virtual environment, install Python requirements and fetch front‑end packages.
This also ensures a `.env` file exists

```shell
make install
```

**_Other useful commands:_**

```shell
make backend    # starts the FastAPI backend server
make frontend   # starts the React frontend server
make cli        # starts the terminal application
make bot        # starts the Telegram bot
make gradio     # runs the web demo using Gradio
```

### Docker

To build and start the project using Docker, run:

```shell
docker compose up -d --build  # builds the images, creates and starts compose stack
```

**_tips:_**

```shell
docker compose stop     # stop running containers
docker compose start    # restart containers that were previously stopped

docker compose down     # stop and remove containers
docker compose up       # build, create and start containers
```

## Developing

To develop the project further, clone the repository and install dependencies as shown above. The Python code lives in `app/backend` and is organised into agents, services, base classes and settings. The React code resides in app/frontend. You can modify the agent or add new tools in `app/backend/agent/tools.py`; the front‑end can be customised in `app/frontend/src`. The back‑end can be restarted by stopping and re‑running `make backend`.

## Features

-   Chat agent - built with LangChain and OpenAI's models that routes your query to either the classifier or the RAG tool
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

The code in this project is licensed under the Apache License 2.0. See LICENSE.
This distribution also includes a NOTICE file with attribution information.
