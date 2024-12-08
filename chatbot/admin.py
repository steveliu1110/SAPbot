from django.contrib import admin
from .models import Website, ChatSession, Message

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('url', 'chunk_count', 'last_update')
    list_filter = ('url', 'last_update')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'name', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat_session', 'role', 'content', 'timestamp')
    list_filter = ('role', 'timestamp')