from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.views.base import TemplateView, FormView as CustomFormView
from webapp.forms import TaskForm, SearchForm, TaskDeleteForm
from webapp.models import Task, Project

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


class CreateTaskView(PermissionRequiredMixin, CreateView):
    permission_required = "webapp.add_task"
    model = Task
    form_class = TaskForm
    template_name = "task_create.html"

    def get_project(self):
        project_pk = self.request.POST.get("project")
        return get_object_or_404(Project, pk=project_pk)

    def has_permission(self):
        has_permission = super().has_permission()

        if self.request.method == "POST":
            has_permission = (
                has_permission
                and self.get_project().users.filter(pk=self.request.user.pk).exists()
            )
        return has_permission

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect('webapp:task_view', pk=self.object.pk)


class TaskView(DetailView):
    template_name = 'tasks/task_view.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        types = self.object.types.order_by("title")
        context['types'] = types
        return context


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "webapp.change_task_in_own_project"
    form_class = TaskForm
    template_name = "task_update.html"
    model = Task

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return (
            super().has_permission()
            and self.get_object().project.users.filter(pk=self.request.user.pk).exists()
        )


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "webapp.delete_task_in_own_project"
    model = Task
    template_name = "task_delete.html"
    success_url = reverse_lazy('webapp:main_page')

    def has_permission(self):
        return (
                super().has_permission()
                and self.get_object().project.users.filter(pk=self.request.user.pk).exists()
        )