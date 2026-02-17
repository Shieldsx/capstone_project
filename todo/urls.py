from django.urls import path
from .views import (
    TodoListIndexView, 
    TodoListCreateView, 
    TodoListDetailView,
)

app_name = "todo"

urlpatterns = [
    path("", TodoListIndexView.as_view(), name="list_index"),
    path("lists/new/", TodoListCreateView.as_view(), name="list_create"),
    path("lists/<int:pk>/", TodoListDetailView.as_view(), name="list_detail"),
]
