from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Emotion

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmotionForm(forms.ModelForm):
    class Meta:
        model = Emotion
        fields = ['emotion', 'description']
        widgets = {
            'emotion': forms.Select(choices=Emotion.EMOTION_CHOICES),
            'description': forms.Textarea(attrs={'rows': 3}),
        }