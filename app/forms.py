from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = MyUser
        fields = ('email', 'date_of_birth', 'password')

    def clean_password2(self):
         # Check that the two password entries match
         password1 = self.cleaned_data.get("password1")
         password2 = self.cleaned_data.get("password2")
         if password1 and password2 and password1 != password2:
             raise forms.ValidationError("Passwords don't match")
         return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "卵を買う"}),
        }