from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
 path('chatbot/', views.chatbot, name='chatbot'),
    path('notes/', views.notes, name='notes'),
    path('notes/<int:pk>/', views.NotesDetailView.as_view(), name='notes-detail'),
    path('notes/update/<int:pk>/', views.update_note, name='update-note'),
    path('notes/share/<int:pk>/', views.share_note, name='share-note'),
    path('notes/delete/<int:pk>/', views.delete_note, name='delete-note'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
    path('homework', views.homework,name="homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete-homework"),

    path('youtube', views.youtube,name="youtube"),

    path('todo', views.todo,name="todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete-todo"),

    path('books', views.books,name="books"),

    path('dictionary', views.dictionary,name="dictionary"),

    path('wiki', views.wiki,name="wiki"),
 path('chat/', views.chat, name='chat'),
    path('chat/user/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('expense', views.expense,name="expense"),
    path('sendemail', views.send_email,name="sendemail"),
    path('upload', views.upload_file,name="upload"),
    #path('download/<int:file_id>/', views.download_file, name='download'),
    path('showfile', views.file_list,name="showfile"),
    path('logout/', views.custom_logout, name='logout'),
    path('search-user/', views.search_user, name='search_user'),
    #path('send-file/<int:user_id>/', views.send_file, name='send_file'),
    path('send-file/<int:user_id>/', views.send_file, name='send_file'),
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),
path('received-files/', views.received_files, name='received_files'),
]
