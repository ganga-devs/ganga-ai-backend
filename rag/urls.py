from django.urls import path

from . import views

app_name = "rag"
urlpatterns = [
    path("health", views.health, name="health"),
]
