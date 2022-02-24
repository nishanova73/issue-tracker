from django.db import models

# Create your models here.
from webapp.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    description = models.CharField(max_length=200, null=False, blank=False, verbose_name="Description",
                                   validators=(MinLengthValidator(20),))
    detailed_description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Detailed_description",
                                            validators=(MinLengthValidator(15),))
    statuses = models.ForeignKey('webapp.StatusModel', default='new', on_delete=models.PROTECT,
                                 related_name='status', verbose_name="Status")
    project = models.ForeignKey('webapp.Project', default=None, on_delete=models.PROTECT,
                                related_name='tasks', verbose_name="Project")
    types = models.ManyToManyField('webapp.TypeModel', max_length=15,  related_name='types')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date changed")

    def get_absolute_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.pk}. {self.description}."

    class Meta:
        db_table = 'Tasks'
        verbose_name = 'task'
        verbose_name_plural = 'tasks'


class StatusModel(models.Model):
    title = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return f"{self.pk} - {self.title}"

    class Meta:
        db_table = 'Statuses'
        verbose_name = 'status'
        verbose_name_plural = 'statuses'


class TypeModel(models.Model):
    title = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return f"{self.pk} - {self.title}"

    class Meta:
        db_table = 'Types'
        verbose_name = 'type'
        verbose_name_plural = 'types'


class Project(models.Model):
    date_started = models.DateField(verbose_name="Date started", null=False, blank=False)
    date_finished = models.DateField(verbose_name="Date finished", null=True, blank=True)
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name="Title",
                             validators=(MinLengthValidator(7),))
    description = models.TextField(max_length=200, null=False, blank=False, verbose_name="Description",
                                   validators=(MinLengthValidator(15),))
    users = models.ManyToManyField(User, related_name='projects', verbose_name="Users of project")

    def get_absolute_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.pk}:{self.title}."

    class Meta:
        db_table = 'Projects'
        verbose_name = 'project'
        verbose_name_plural = 'projects'