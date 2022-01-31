from django.urls import path
from django.views.generic import RedirectView
from webapp.views import (IndexView,
                          CreateTaskView,
                          TaskView,
                          TaskUpdateView,
                          TaskDeleteView,
                          CreateProjectView,
                          ProjectView,
                          ProjectUpdateView,
                          ProjectDeleteView,
                          IndexView_,
                          ProjectCreateTask
                          )



urlpatterns = [
    path('', IndexView.as_view(), name="main_page"),
    path('tasks/', RedirectView.as_view(pattern_name="main_page")),
    path('task/create_task/', CreateTaskView.as_view(), name="task_add"),
    path('task_view/<int:pk>/', TaskView.as_view(template_name="task_view.html"), name="task_view"),
    path('task_view/<int:pk>/update/', TaskUpdateView.as_view(), name="task_update"),
    path('task_view/<int:pk>/delete/', TaskDeleteView.as_view(), name="task_delete"),
    path('project/create_project/', CreateProjectView.as_view(), name="project_add"),
    path('project_view/<int:pk>/', ProjectView.as_view(template_name="projects/view.html"), name="project_view"),
    path('project_view/<int:pk>/update/', ProjectUpdateView.as_view(), name="project_update"),
    path('project_view/<int:pk>/delete/', ProjectDeleteView.as_view(), name="project_delete"),
    path('projects/', IndexView_.as_view(), name="main_page2"),
    path('project_view/<int:pk>/task/add/', ProjectCreateTask.as_view(), name="project_task_add"),
]