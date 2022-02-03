from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.views.base import TemplateView, FormView as CustomFormView
from webapp.forms import TaskForm, SearchForm, TaskDeleteForm
from webapp.models import Task

class IndexView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "index.html"
    paginate_by = 10
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            print(self.search_value)
            query = Q(description__icontains=self.search_value) | Q(detailed_description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("-updated_at")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['form'] = SearchForm(initial={"search": self.search_value})
            context['search'] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class CreateTaskView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_create.html"


class TaskView(DetailView):
    template_name = 'tasks/task_view.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        types = self.object.types.order_by("title")
        context['types'] = types
        return context

class TaskUpdateView(UpdateView):
    form_class = TaskForm
    template_name = "task_update.html"
    model = Task


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = reverse_lazy('main_page')

    def dispatch(self, request, *args, **kwargs):
        if self.request.method == "POST":
            self.object_form = TaskDeleteForm(instance=self.get_object(), data=self.request.POST)
        else:
            self.object_form = TaskDeleteForm()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.object_form
        return context

    def post(self, request, *args, **kwargs):
        if self.object_form.is_valid():
            return super().delete(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)