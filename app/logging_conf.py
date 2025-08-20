import logging
import warnings
import os
from langchain_core._api.deprecation import LangChainDeprecationWarning

def configure_logging(quiet = True) -> None:
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    if quiet:
        logging.getLogger("transformers").setLevel(logging.ERROR)
        warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
        warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


