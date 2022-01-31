from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, ListView, DetailView, CreateView

from webapp.views.base import TemplateView, FormView as CustomFormView
from webapp.forms import TaskForm, SearchForm
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


class TaskUpdateView(FormView):
    form_class = TaskForm
    template_name = 'task_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super(TaskUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={"pk": self.task.pk})

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get("pk"))

class TaskDeleteView(TemplateView):
    def get(self, request, pk=None, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'task_delete.html', {'task': task})

    def post(self, request, pk=None, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('main_page')