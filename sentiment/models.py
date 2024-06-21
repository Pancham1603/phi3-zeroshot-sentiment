from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class ChatInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.timestamp.time().strftime("%H:%M:%S")} | {self.timestamp.date().strftime("%Y-%m-%d")}] {self.user.username}'

class Chat(models.Model):
    chat = models.ForeignKey(ChatInstance, on_delete=models.CASCADE)
    message = models.TextField(default='',blank=True)
    reply = models.TextField(default='',blank=True)
    sentiment = models.TextField(default='',blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.chat.user.username}: {self.message[:50]}'