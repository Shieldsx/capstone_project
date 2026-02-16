from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import TodoList


class TodoListIndexView(LoginRequiredMixin, ListView):
    model = TodoList
    template_name = "todo/list_index.html"
    context_object_name = "lists"

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user).order_by("-updated_on", "-created_on")


class TodoListCreateView(LoginRequiredMixin, CreateView):
    model = TodoList
    template_name = "todo/list_form.html"
    fields = ["name"]
    success_url = reverse_lazy("todo:list_index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "List created.")
        return super().form_valid(form)
