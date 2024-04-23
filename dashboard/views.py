import os
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import random
# Create your views here.


def home(request):
    return render(request, 'dashboard/home.html')
#Method to open notes feature and create new notes
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import NotesForm
from .models import Notes
from django.contrib.auth.decorators import login_required

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(request, f"Notes Added from {request.user.username} successfully!")
            return redirect("notes")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

@login_required
def update_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    form = NotesForm(request.POST or None, instance=note)
    if form.is_valid():
        form.update_instance(note)
        messages.success(request, f"Note Updated from {request.user.username} successfully!")
        return redirect('notes')
    return render(request, 'dashboard/note_update.html', {'form': form})

@login_required
def share_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    # Add your share logic here
    return redirect('notes')

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    note.delete()
    messages.success(request, f"Note Deleted from {request.user.username} successfully!")
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes


#Method to open Homework feature and create a new homework along with assigning a date of completion to it
@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f'Homework Added from {request.user.username}!!')
            return redirect("homework")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user).order_by("due")
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks': homework,
        'homeworks_done': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)

#Method to update the completion status of a homework
@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")

#Method to delete an existing homework
@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

#Method to open Youtube feature and to provide the response according to the search text
def youtube(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardFom()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)

#Method to create a todo list using todo feature
@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                fnished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request, f"Todo Added from {request.user.username}!!")
            return redirect("todo")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form': form,
        'todos': todo,
        'todos_done': todos_done
    }
    return render(request, "dashboard/todo.html", context)

#Method to update completion status of an existing todo
@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")

#Method to delete an existing todo
@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

#Method to find for the ebook stack based using the keyword searched
def books(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardFom()
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)

#Method to perform the dictionary function
def dictionary(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text = request.POST['text']
        #API used is dictionaryapi
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            #example = answer[0]['meanings'][0]['definitions'][0]['example']
            #synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                #'example': example,
                #'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardFom()
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)

#Method to perform the WikiPedia search
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardFom()
        try:
            search = wikipedia.page(text)
        except wikipedia.DisambiguationError as e:
            text = random.choice(e.options)
        s = wikipedia.page(text)
        context = {
            'form': form,
            'title': s.title,
            'link': s.url,
            'details': s.summary
        }
        return render(request, "dashboard/wiki.html", context)
    else:
        form = DashboardFom()
        context = {
            'form': form
        }
    return render(request, 'dashboard/wiki.html', context)
#Method to manage the expenses and to create and maintain an e-wallet(Profile class is referring to that!)
@login_required
def expense(request):
    profiles=Profile.objects.filter(user = request.user).first()
    expenses=Expense.objects.filter(user = request.user)
    profile = Profile(user = request.user)
    profile.save()

    if request.method == "POST":
        text = request.POST.get('text')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')
        expense = Expense(name=text , amount = amount , expense_type=expense_type , user = request.user)
        expense.save()

        # Updating the wallet status after recieving every transaction history
        if expense_type=='Positive':
            profiles.balance += float(amount)
            profiles.income += float(amount)
        else:
            profiles.expenses += float(amount)
            profiles.balance -= float(amount)
        profiles.save()
        return redirect("expense")
    context={
        'profiles':profiles,
        'expenses':expenses
         }
    return render(request, 'dashboard/expense.html', context)

#Method to perform new user registration
def register(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f"Account Created for {username}!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }

    return render(request, 'dashboard/register.html', context)

#Method for profile section (which keeps track of pending Homework and Todos)
@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homework_done = False
    else:
        homework_done = True
    if len(todos) == 0:
        todos_done = False
    else:
        todos_done = True
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        ' todos_done':  todos_done
    }

    return render(request, "dashboard/profile.html", context)
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.shortcuts import render
from .forms import EmailForm

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient = form.cleaned_data['recipient']

            # Prepare the email message
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[recipient],
            )

            # Attach files to the email, if any
            for file in request.FILES.getlist('attachments'):
                email.attach(file.name, file.read(), file.content_type)

            # Send the email
            email.send()

            return render(request, 'dashboard/email_sent.html')
    else:
        form = EmailForm()
    return render(request, 'dashboard/send_email.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadedFile
from .forms import FileUploadForm
from django.http import HttpResponse
import os

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('showfile')
    else:
        form = FileUploadForm()
    return render(request, 'dashboard/upload_file.html', {'form': form})

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'dashboard/file_list.html', {'files': files})

def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    file_path = uploaded_file.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response

def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    # Check if the file belongs to the current user
    if file.user == request.user:
        file.delete()
    return redirect('showfile')

# faq_chatbot/views.py

from django.shortcuts import render
from .models import FAQ

def chatbot(request):
    response = None
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        faq = FAQ.objects.filter(question__icontains=user_input).first()
        if faq:
            response = faq.answer
        else:
            response = "Sorry, I couldn't find an answer to your question."
    return render(request, 'dashboard/chatbot.html', {'response': response})
# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Message

def chat(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'dashboard/chat.html', {'users': users})

def chat_with_user(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    messages = Message.objects.filter(sender=request.user, receiver=other_user) | Message.objects.filter(sender=other_user, receiver=request.user)
    return render(request, 'dashboard/chat_with_user.html', {'other_user': other_user, 'messages': messages})

