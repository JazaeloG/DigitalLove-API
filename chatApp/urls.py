from django.urls import path
from . import views

urlpatterns = [
    path('user/chats/', views.get_user_chats, name='user_chats'),
    path('chat/<int:chat_id>/messages/', views.get_chat_messages, name='chat_messages'),
]