from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse
from .models import TodoList, Task



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
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "completed", "due_date"]
    template_name = "todo/task_form.html"
    login_url = "/accounts/login/"  # optional, but explicit

    def get_todo_list(self):
        return get_object_or_404(
            TodoList,
            pk=self.kwargs["pk"],
            owner=self.request.user,
        )

    def form_valid(self, form):
        form.instance.todo_list = self.get_todo_list()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.get_todo_list()
        return context

    def get_success_url(self):
        return reverse("todo:list_detail", kwargs={"pk": self.kwargs["pk"]})

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "todo/task_form.html"
    fields = ["title", "description", "due_date"]

    def get_object(self, queryset=None):
        return get_object_or_404(
            Task,
            pk=self.kwargs["task_pk"],
            todo_list__pk=self.kwargs["list_pk"],
            todo_list__owner=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = get_object_or_404(
            TodoList,
            pk=self.kwargs["list_pk"],
            owner=self.request.user,
        )
        return context

    def get_success_url(self):
        return reverse(
            "todo:list_detail",
            kwargs={"pk": self.kwargs["list_pk"]},
        )
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "todo/task_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Task,
            pk=self.kwargs["task_pk"],
            todo_list__pk=self.kwargs["list_pk"],
            todo_list__owner=self.request.user,
        )

    def get_success_url(self):
        return reverse(
            "todo:list_detail",
            kwargs={"pk": self.kwargs["list_pk"]},
        )