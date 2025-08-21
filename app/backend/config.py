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
        self.base_url = getenv("APP_BASE_URL")
        self.run_mode = getenv("RUN_MODE")

settings = AppConfig()
