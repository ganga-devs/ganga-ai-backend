import logging
import os
import re
import shutil
import subprocess
from typing import Literal, List
from root.settings import environment_variables
from rag.github import download_github_repo
from llama_index.core import ( VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, Settings)
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

def create_directory(directory_path: str) -> None:
    """
    Creates the given directory
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.info(f"file vector_store function create_directory created new directory at {directory_path}")
    except Exception as err:
        logger.warning(f"file vector_store function create_directory error encountered: {err}")

def remove_directory(directory_path: str) -> None:
    """
    Removes a certain directory
    """
    try:
        shutil.rmtree(directory_path)
        logger.info(f"file vector_store function remove_directory removed directory {directory_path}")
    except Exception as err:
        logger.warning(f"file vector_store function create_directory error encountered: {err}")

class Vector_Store():
    """
    TODOS
    1. Use pg vector instead of json
    """

    cache_path = environment_variables["CACHE_PATH"]
    embedding_model = environment_variables["EMBEDDING_MODEL"]
    llm_model = environment_variables["LLM_MODEL"]
    data_urls = environment_variables["DATA_URLS"]
    raw_data_path = os.path.join(cache_path, "raw")
    processed_data_path = os.path.join(cache_path, "processed")
    vector_store_path = os.path.join(cache_path, "vector_store")
    Settings.embed_model = HuggingFaceEmbedding(model_name=embedding_model)
    vector_store = None

    def __init__(self):
        if self.vector_store_exists():
            self.load_vector_store()
        else:
            self.create_vector_store()

    def vector_store_exists(self) -> bool:
        """
        Check if the vector store already exists and has only indices in json files
        """
        logger.info(f"file: vector_store method: vector_store_exists vector_store_path: {self.vector_store_path}")
        if os.path.isdir(self.vector_store_path):
            for file_name in os.listdir(self.vector_store_path):
                if file_name.endswith(".json"):
                    return True
        return False

    def generate_text_files_from_sphinx_files(self, input_sphinx_dir: str, output_txt_dir):
        """
        Generates text files from sphinx files
        """

        build_command = ["sphinx-build", "-b", "text", input_sphinx_dir, output_txt_dir]

        subprocess.run(build_command, check=True)

        doctrees_path = os.path.join(output_txt_dir, ".doctrees")
        if os.path.exists(doctrees_path):
            shutil.rmtree(doctrees_path)

    def consume_ganga_docs(self) -> None:
        ganga_sphinx_files_path = os.path.join(self.raw_data_path, "ganga/doc")
        ganga_txt_files_path = os.path.join(self.processed_data_path, "ganga/doc")
        create_directory(ganga_txt_files_path)
        self.generate_text_files_from_sphinx_files(input_sphinx_dir=ganga_sphinx_files_path, output_txt_dir=ganga_txt_files_path)
        documents = SimpleDirectoryReader(input_dir=ganga_sphinx_files_path, recursive=True).load_data()
        self.vector_store = VectorStoreIndex.from_documents(documents)
        self.vector_store.storage_context.persist(persist_dir=self.vector_store_path)

    def consume_data(self, dir_list: List[str]):
        for dir in dir_list:
            match dir:
                case "cache/raw/ganga/doc":
                    self.consume_ganga_docs()
                case _:
                    logger.info(f"file: vector_store method: consume_data unhandled type of data: {dir}")

    def create_list_of_directories_to_consume(self, raw_cache_path: str) -> List[str]:
        """
        Create a list of directories to consume data from which the rag will be built
        """

        dir_list = []
        try:
            for subdir in os.listdir(raw_cache_path):
                subdir_path = os.path.join(raw_cache_path, subdir)
                if subdir == 'ganga':
                    dir_list.append(os.path.join(subdir_path, 'doc'))
                else:
                    dir_list.append(subdir_path)
        except Exception as err:
            print(f"file: vector_store method: create_list_of_directories_to_consume error: {err}")
        return dir_list

    def download_intial_data(self, url: str, download_path) -> None:
        url_type = type_of_url(url=url)
        match url_type:
            case "GITHUB":
                download_github_repo(github_url=url, download_path=download_path)
            case "UNKNOWN":
                logger.warning(f"file: vector_store method: download_data the unknown type of url encountered: {url}")

    def create_vector_store(self):
        for directory_path in (self.raw_data_path, self.processed_data_path, self.vector_store_path):
            create_directory(directory_path)

        for url in self.data_urls:
            self.download_intial_data(url=url, download_path=self.raw_data_path)

        dir_list = self.create_list_of_directories_to_consume(self.raw_data_path)
        self.consume_data(dir_list=dir_list)

        for directory_path in (self.raw_data_path, self.processed_data_path):
            remove_directory(directory_path=directory_path)

    def load_vector_store(self):
        storage_context = StorageContext.from_defaults(persist_dir=self.vector_store_path)
        self.vector_store = load_index_from_storage(storage_context)
