from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, ListView, DetailView, CreateView
from webapp.views.base import TemplateView
from webapp.forms import ProjectForm, TaskForm
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


class CreateProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create.html"

class ProjectView(DetailView):
    template_name = 'projects/view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectUpdateView(FormView):
    form_class = ProjectForm
    template_name = 'projects/update.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = self.get_object()
        return super(ProjectUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.project
        return kwargs

    def form_valid(self, form):
        self.project = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_view', kwargs={"pk": self.project.pk})

    def get_object(self):
        return get_object_or_404(Project, pk=self.kwargs.get("pk"))

class ProjectDeleteView(TemplateView):
    def get(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'projects/delete.html', {'project': project})

    def post(self, request, pk=None, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return redirect('main_page2')


class ProjectCreateTask(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/create_task.html'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.save()
        return redirect('project_view', pk=project.pk)