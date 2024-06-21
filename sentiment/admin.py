from django.contrib import admin
from .models import ChatInstance, Chat

class ChatInstanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp')
    search_fields = ('user__username',)
    list_filter = ('timestamp',)

class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat', 'message', 'reply', 'sentiment', 'timestamp')
    search_fields = ('chat__user__username', 'message', 'reply', 'sentiment')
    list_filter = ('timestamp',)

admin.site.register(ChatInstance, ChatInstanceAdmin)
admin.site.register(Chat, ChatAdmin)
