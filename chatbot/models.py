from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Website(models.Model):
    url = models.URLField(max_length=200, unique=True)
    chunk_count = models.IntegerField()
    last_update = models.TextField()

    def __str__(self):
        return self.url

class ChatSession(models.Model):
    """
    Represents a chat session between a user and the GPT model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sessions")
    name = models.CharField(max_length=100, default="Empty Session", help_text="Unique name for the session")
    session_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, help_text="Unique identifier for the session")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatSession {self.session_id} for {self.user.username}"

class Message(models.Model):
    """
    Represents individual messages exchanged in a chat session.
    """
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"