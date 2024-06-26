from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('news/', views.news, name='news'),
    path('notes/', views.notes, name='notes'),
    path('notes/update/<int:note_id>/', views.update_note, name='update_note'),
    path('notes/delete/<int:pk>/', views.delete_note, name='delete_note'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
    path('homework/', views.homework, name="homework"),
    path('update_homework/<int:pk>/', views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>/', views.delete_homework, name="delete-homework"),
    path('youtube/', views.youtube, name="youtube"),
    path('todo/', views.todo, name="todo"),
    path('update_todo/<int:pk>/', views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>/', views.delete_todo, name="delete-todo"),
    path('books/', views.books, name="books"),
    path('dictionary/', views.dictionary, name="dictionary"),
    path('wiki/', views.wiki, name="wiki"),
    path('expense/', views.expense, name="expense"),
    path('sendemail/', views.send_email, name="sendemail"),
    path('upload/', views.upload_file, name="upload"),
    path('showfile/', views.file_list, name="showfile"),
    path('logout/', views.custom_logout, name='logout'),
    path('search-user/', views.search_user, name='search_user'),
    path('send-file/<int:user_id>/', views.send_file, name='send_file'),
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),
    path('received-files/', views.received_files, name='received_files'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('faq/', views.faq, name='faq'),
    path('add_faq/', views.add_faq, name='add_faq'),
    path('update_profile/', views.update_profile, name='update_profile'),
  path('chat/', views.index, name='select_user'),
    path('chat/<str:room_name>/', views.chatroom, name='chatroom'),
path('reply/', views.reply_message, name='reply_message'),



    path('knowledge-base/', views.knowledge_base_list, name='knowledge_base_list'),
    path('knowledge-base/add/', views.add_knowledge_base, name='add_knowledge_base'),
    path('knowledge-base/<int:pk>/', views.knowledge_base_detail, name='knowledge_base_detail'),
    # other paths...


 
]
