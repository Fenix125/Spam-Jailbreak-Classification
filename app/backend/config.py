from os import getenv
from dotenv import load_dotenv
load_dotenv()

class AppConfig():
    def __init__(self):
        self.openai_api_key = getenv("OPENAI_API_KEY")
        self.openai_model = getenv("OPENAI_MODEL")
        self.classifier_model = getenv("CLASSIFIER_MODEL")
        self.embed_model = getenv("EMBED_MODEL")
        self.file_path = getenv("FILE_PATH")
        self.backend_host = getenv("APP_BACKEND_HOST")
        self.backend_port = getenv("APP_BACKEND_PORT")

        self.frontend_host = getenv("APP_FRONTEND_HOST")
        self.frontend_port = getenv("APP_FRONTEND_PORT")

        self.backend_adress = f"http://{self.backend_host}:{self.backend_port}/api"
        self.frontend_adress = f"http://{self.frontend_host}:{self.frontend_port}"

        self.run_mode = getenv("RUN_MODE")

        self.telegram_bot_token = getenv("TELEGRAM_BOT_TOKEN")

settings = AppConfig()
