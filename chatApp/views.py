from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Chat, Message

@login_required
def get_user_chats(request):
    chats = request.user.chats.all()
    data = [{'id': chat.id, 'usernames': [user.username for user in chat.users.all()]} for chat in chats]
    return JsonResponse(data, safe=False)

@login_required
def get_chat_messages(request,chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all().order_by('timestamp')
    data = [{'sender': message.sender.username, 'content': message.content, 'timestamp': message.timestamp} for message in messages]
    return JsonResponse(data, safe=False)
