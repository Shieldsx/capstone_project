from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .models import TodoList


class TodoListIndexView(LoginRequiredMixin, ListView):
    model = TodoList
    template_name = "todo/list_index.html"
    context_object_name = "lists"

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user).order_by(
            "-updated_on", "-created_on"
        )


class TodoListCreateView(LoginRequiredMixin, CreateView):
    model = TodoList
    template_name = "todo/list_form.html"
    fields = ["name"]
    success_url = reverse_lazy("todo:list_index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "List created.")
        return super().form_valid(form)


class TodoListDetailView(LoginRequiredMixin, DetailView):
    model = TodoList
    template_name = "todo/list_detail.html"
    context_object_name = "todo_list"

    def get_object(self, queryset=None):
        return get_object_or_404(
            TodoList,
            pk=self.kwargs["pk"],
            owner=self.request.user,
        )
