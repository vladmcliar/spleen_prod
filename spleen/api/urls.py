from django.urls import path
from .views import RegisterView, login_view, EmotionCreateView, api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('emotions/', EmotionCreateView.as_view(), name='create_emotion'),
]