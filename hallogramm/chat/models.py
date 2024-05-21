from django.db import models

import uuid

from django.urls import reverse_lazy
from account.models import Profile


class Chat(models.Model):
    name = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    users = models.ManyToManyField(Profile, related_name='chat_users', blank=True)

    def __str__(self):
        return f'Chat {self.name}'

    def get_absolute_url(self):
        return reverse_lazy(viewname='show_chat', kwargs={'chat_uuid': self.uuid})


class Message(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='user_message')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f'Message: {self.text},'
                f'author: {self.author.user.username},'
                f'chat name: {self.chat.name}'
                f'time_create: {self.time_create},'
                f'time_update: {self.time_update}.')
