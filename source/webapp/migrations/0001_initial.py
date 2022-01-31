# Generated by Django 4.0.1 on 2022-01-31 07:37

from django.db import migrations, models
import django.db.models.deletion
import webapp.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_started', models.DateField(verbose_name='Date started')),
                ('date_finished', models.DateField(blank=True, null=True, verbose_name='Date finished')),
                ('title', models.CharField(max_length=20, validators=[webapp.validators.MinLengthValidator(7)], verbose_name='Title')),
                ('description', models.TextField(max_length=200, validators=[webapp.validators.MinLengthValidator(15)], verbose_name='Description')),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
                'db_table': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='StatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
                'db_table': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='TypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'type',
                'verbose_name_plural': 'types',
                'db_table': 'Types',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, validators=[webapp.validators.MinLengthValidator(20)], verbose_name='Description')),
                ('detailed_description', models.TextField(blank=True, max_length=2000, null=True, validators=[webapp.validators.MinLengthValidator(15)], verbose_name='Detailed_description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date changed')),
                ('project', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='project', to='webapp.project', verbose_name='Project')),
                ('statuses', models.ForeignKey(default='new', on_delete=django.db.models.deletion.PROTECT, related_name='status', to='webapp.statusmodel', verbose_name='Status')),
                ('types', models.ManyToManyField(max_length=15, related_name='types', to='webapp.TypeModel')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
                'db_table': 'Tasks',
            },
        ),
    ]