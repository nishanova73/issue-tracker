from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Task, TypeModel, StatusModel, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = []
        widgets = {
            'detailed_description': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
            'types': forms.CheckboxSelectMultiple,
        }

    def clean_description(self):
        if len(self.cleaned_data.get('description')) < 20:
            raise ValidationError(f"The description field must be more than 20 symbols!")
        return self.cleaned_data.get('description')

    def clean_detailed_description(self):
        if len(self.cleaned_data.get('detailed_description')) > 2000:
            raise ValidationError(f"The detailed description field must be less than 2000 symbols!")
        return self.cleaned_data.get('detailed_description')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Search")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = []
        widgets = {
            'date_started': forms.SelectDateWidget(),
            'date_finished': forms.SelectDateWidget(),
            'user': forms.CheckboxSelectMultiple,
        }


class TaskDeleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("description",)

    def clean_title(self):
        print(self.instance.title, self.cleaned_data.get("description"))
        if self.instance.title != self.cleaned_data.get("description"):
            print('error')
            raise ValidationError("Description isn't valid")
        return self.cleaned_data.get("description")

class ProjectDeleteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title",)

    def clean_title(self):
        print(self.instance.title, self.cleaned_data.get("title"))
        if self.instance.title != self.cleaned_data.get("title"):
            print('error')
            raise ValidationError("Title isn't valid")
        return self.cleaned_data.get("title")