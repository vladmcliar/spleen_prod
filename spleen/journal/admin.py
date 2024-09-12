from django.contrib import admin
from .models import JournalEntry, Emotion

admin.site.register(JournalEntry)
admin.site.register(Emotion)