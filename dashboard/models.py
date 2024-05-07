from django.db import models
from django.contrib.auth.models import User

# Create your models here.


from django.urls import reverse
from django.utils import timezone

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notes-detail', args=[str(self.id)])

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

TYPE = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative')
    )

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income = models.FloatField(default=0)
    expenses = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.user)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    expense_type = models.CharField(max_length=100,choices=TYPE)

    def __str__(self):
        return self.name
from django.db import models

from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.message}"
    
from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
