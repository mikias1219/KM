import os
import random
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from .models import Notes, UploadedFile
from .forms import NotesForm, FileUploadForm
from django.core.mail import EmailMessage
from .forms import EmailForm
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

from .models import News
@login_required
def home(request):
    news_items = News.objects.all().order_by('-date_posted')[:5]  # Get the latest 5 news items
    context = {'news_items': news_items}
    return render(request, 'dashboard/home.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Notes
from .forms import NotesForm

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(request, f"Notes added successfully!")
            return redirect("notes")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

@login_required
def update_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id, user=request.user)
    if request.method == "POST":
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f"Note updated successfully!")
            return redirect("notes")
    else:
        form = NotesForm(instance=note)
    context = {'form': form, 'note': note}
    return render(request, 'dashboard/note_update.html', context)


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    note.delete()
    messages.success(request, f"Note Deleted from {request.user.username} successfully!")
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model = Notes

# Add your other views here...


# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

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

@login_required
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

@login_required
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


@login_required
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

@login_required
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

#def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    file_path = uploaded_file.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    # Check if the file belongs to the current user
    if file.user == request.user:
        file.delete()
    return redirect('showfile')

# faq_chatbot/views.py

from django.shortcuts import render
from .models import FAQ

@login_required
def chatbot(request):
    faq_questions = FAQ.objects.all()
    response = None

    if request.method == 'POST':
        question_id = request.POST.get('faq_question')
        selected_faq = get_object_or_404(FAQ, id=question_id)
        response = selected_faq.answer

    context = {
        'faq_questions': faq_questions,
        'response': response,
    }
    return render(request, 'dashboard/chatbot.html', context)
# views.py



def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to a specific URL after logout

@login_required
def search_user(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)
    return render(request, 'dashboard/search_user.html', {'users': users, 'query': query})

@login_required
def send_file(request, user_id):
    selected_user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.sender = request.user  # Save sender's information
            uploaded_file.user = selected_user
            uploaded_file.save()
            # Redirect to the same page to prevent duplicate form submissions
            return redirect('send_file', user_id=user_id)
    else:
        form = FileUploadForm()

    # Only show files that belong to the currently logged-in user
    files = UploadedFile.objects.filter(user=request.user)

    return render(request, 'dashboard/send_file.html', {'selected_user': selected_user, 'form': form, 'files': files})


@login_required
def received_files(request):
    # Retrieve files that the currently logged-in user has received
    files = UploadedFile.objects.filter(user=request.user)
    
    return render(request, 'dashboard/received_files.html', {'files': files})

@login_required
def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(uploaded_file.file.name)
    return response
from django.shortcuts import render
from .models import News

@login_required
def news(request):
    news_items = News.objects.all().order_by('-date_posted')
    context = {'news_items': news_items}
    return render(request, 'dashboard/news.html', context)

# views.py
from django.shortcuts import render, redirect
from .models import Announcement
from .forms import AnnouncementForm

@login_required
def announcements(request):
    announcements = Announcement.objects.all().order_by('-date_posted')
    return render(request, 'dashboard/announcements.html', {'announcements': announcements})
from django.shortcuts import render, redirect
from .forms import AnnouncementForm
from .models import Announcement

@login_required
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.creator = request.user  # Assuming creator is the correct field name
            announcement.save()
            return redirect('announcements')  # Assuming 'announcements' is the URL name for listing announcements
    else:
        form = AnnouncementForm()
    return render(request, 'dashboard/create_announcement.html', {'form': form})
from django.shortcuts import render
from .models import FAQ
from .forms import FAQForm

@login_required
def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'dashboard/faq.html', {'faqs': faqs})

@login_required
def add_faq(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FAQForm()
    return render(request, 'dashboard/add_faq.html', {'form': form})

