
from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','is_finished']

class DashboardFom(forms.Form):
    text = forms.CharField(max_length=100, label="Enter your Search : ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
# forms.py
from django import forms

from django import forms

class EmailForm(forms.Form):
    recipient = forms.EmailField(label='To')
    cc = forms.EmailField(label='CC', required=False)
    bcc = forms.EmailField(label='BCC', required=False)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
