from django.apps import AppConfig
from rag.vector_store import Vector_Store


class RagConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rag"
    vector_store = None

    def ready(self):
        if self.vector_store is None:
            self.vector_store = Vector_Store() 
