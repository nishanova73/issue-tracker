from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.views.base import TemplateView
from webapp.forms import ProjectForm, TaskForm, ProjectDeleteForm, ProjectUsersForm
from webapp.models import Project, Task


class IndexView_(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "projects/index2.html"
    paginate_by = 3
    paginate_orphans = 0

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-date_started")


class CreateProjectView(PermissionRequiredMixin, CreateView):
    permission_required = "webapp.add_project"
    model = Project
    form_class = ProjectForm
    template_name = "projects/create.html"

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super(CreateProjectView, self).form_valid(form)
        self.object.users.add(self.request.user)
        return response


class ProjectView(DetailView):
    template_name = 'projects/view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "webapp.change_project"
    form_class = ProjectForm
    template_name = "projects/update.html"
    model = Project

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "webapp.delete_project"
    model = Project
    template_name = "projects/delete.html"
    success_url = reverse_lazy('webapp:main_page2')

    # def dispatch(self, request, *args, **kwargs):
    #     if self.request.method == "POST":
    #         self.object_form = ProjectDeleteForm(instance=self.get_object(), data=self.request.POST)
    #     else:
    #         self.object_form = ProjectDeleteForm()
    #     return super().dispatch(request, *args, **kwargs)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = self.object_form
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     if self.object_form.is_valid():
    #         return super().delete(request, *args, **kwargs)
    #     return super().get(request, *args, **kwargs)


class ProjectCreateTask(PermissionRequiredMixin, CreateView):
    permission_required = "webapp.add_task_in_own_project"
    model = Task
    template_name = 'projects/create_task.html'
    form_class = TaskForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        project.save()
        return redirect('webapp:task_view', pk=task.pk)

    def has_permission(self):
        return super().has_permission() or self.request.user.username == self.get_object().user_pr


class ChangeProjectUsers(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/change_users.html'
    form_class = ProjectUsersForm
    permission_required = 'webapp.change_user_in_own_project'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return (
                super().has_permission()
                and self.get_object().users.filter(pk=self.request.user.pk).exists()
        )


class ProjectUsers(DetailView):
    model = Project
    template_name = 'projects/project_users.html'
    pk_url_kwarg = 'project_pk'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})