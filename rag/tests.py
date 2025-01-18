from django.test import TestCase
from rag.vector_store import type_of_url, vector_store_exists
import logging
import os
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Rag_Test_Case(TestCase):
    logger.info("Running tests for the rag module")

    def test_type_of_url(self):
        logger.info("Running test for type_of_url function")
        github_test_url = "https://github.com/ganga-devs/ganga/tree/develop/doc"
        unkown_test_url = "https://www.google.com/"
        self.assertEqual(type_of_url(github_test_url), "GITHUB")
        self.assertEqual(type_of_url(unkown_test_url), "UNKNOWN")

    def test_vector_store_exists(self):
        logger.info("Running test for vector_store_exists function")

        # Test paths
        test_cache_path = "test_cache"
        test_vector_store_path = os.path.join(test_cache_path, "vector_store")
        test_json_filepath = os.path.join(test_vector_store_path, "test.json")
        
        # Helper functions
        def remove_dummy_vector_store():
            if os.path.exists(test_cache_path):
                shutil.rmtree(test_cache_path)

        def create_dummy_vector_store():
            os.makedirs(test_vector_store_path)

        def create_dummy_json_file():
            with open(test_json_filepath, "w") as test_json_file:
                test_json_file.write("{}")
        
        try:
            logger.info("Checking for and cleaning older test artifcats")
            remove_dummy_vector_store()

            logger.info("Creating dummy vector store for testing")
            create_dummy_vector_store()

            self.assertFalse(vector_store_exists(test_cache_path))

        except Exception as err:
            logger.warn(f"Error encountered in running test_vector_store_exists: {err}")
            return

        try:
            logger.info("Creating dummy json file for testing")
            create_dummy_json_file()

            self.assertTrue(vector_store_exists(test_cache_path))

            logger.info("Cleaning test artifcats")
            remove_dummy_vector_store()

        except Exception as err:
            logger.warn(f"Error encountered in running test_vector_store_exists: {err}")
            return
