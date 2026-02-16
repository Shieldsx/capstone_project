from django.urls import path
from .views import TodoListIndexView, TodoListCreateView

app_name = "todo"

urlpatterns = [
    path("", TodoListIndexView.as_view(), name="list_index"),
    path("lists/new/", TodoListCreateView.as_view(), name="list_create"),
]
