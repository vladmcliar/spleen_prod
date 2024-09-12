from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    emotion = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Emotion(models.Model):
    EMOTION_CHOICES = (
        ('😊', 'Happy'),
        ('😢', 'Sad'),
        ('😆', 'Laughing'),
        ('😐', 'Neutral'),
        ('😠', 'Angry'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotions')
    emotion = models.CharField(max_length=1, choices=EMOTION_CHOICES)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.get_emotion_display()}"