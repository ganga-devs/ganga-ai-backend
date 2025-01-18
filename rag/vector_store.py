from typing import Literal
import logging
import os
import re
from root.settings import Environtment_Variables, environment_variables
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
    Settings,
)
from llama_index.core.storage import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def type_of_url(url: str) -> Literal["GITHUB", "UNKNOWN"]:
    """
    Determines the type of a given data url
    """
    match url:
        case url if re.match(r"^https?://(www\.)?github\.com(/|$)", url):
            url_type = "GITHUB"
        case _:
            url_type = "UNKNOWN"
    logger.info(f"file: vector_store function: type_of_url input: {url} output: {url_type}")
    return url_type

# TODO: move to pg vector over json files
def vector_store_exists(cache_path: str) -> bool:
    """
    Check if the vector store already exists and has only indices in json files
    """
    logger.info(f"file: vector_store function: vector_store_exists cache_path: {cache_path}")
    vector_store_path = os.path.join(cache_path, "vector_store")
    if os.path.isdir(vector_store_path):
        for file_name in os.listdir(vector_store_path):
            if file_name.endswith(".json"):
                return True
    return False

def type_of_file():
    pass

# TODO: write converters for all types
def convert_sphinx_to_txt():
    pass

def create_vector_store():
    pass

def load_vector_store():
    pass

def startup():
    if vector_store_exists(environment_variables["CACHE_PATH"]):
        return load_vector_store()
    else:
        return create_vector_store()
