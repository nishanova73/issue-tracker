# Generated by Django 4.0.1 on 2022-02-21 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_project_author_alter_project_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='author',
        ),
    ]