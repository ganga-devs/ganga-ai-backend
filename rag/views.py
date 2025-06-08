from django.http import HttpResponse
from rag.serializers import VectorStoreSerializer
from rag.vector_store import vector_store
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


@api_view(["GET"])
def health(request):
    return HttpResponse("ok")


@api_view(["POST"])
def query(request, *args, **kwargs):
    if request.method == "POST":
        serializer = VectorStoreSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.data["query"]
            print(f"DEBUGPRINT[20]: views.py:17: query={query}")
            llm_response = vector_store.query_vector_store(query=query)
            print(f"DEBUGPRINT[21]: views.py:20: llm_response={llm_response}")
            return Response({"success": "success"}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
