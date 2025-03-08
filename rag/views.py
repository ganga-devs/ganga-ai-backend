from django.http import HttpResponse
import json
from rag.vector_store import vector_store

def health(request):
    return HttpResponse("ok")

def query(request):
    if request.method == "POST":
        data = json.loads(request.body)
        llm_response = vector_store.query_vector_store(data)
        return HttpResponse(f"{llm_response}")
