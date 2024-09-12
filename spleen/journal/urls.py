from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('emotion/new/', views.emotion_create, name='emotion_create'),
    path('emotion/<int:pk>/edit/', views.emotion_update, name='emotion_update'),
    path('emotion/<int:pk>/delete/', views.emotion_delete, name='emotion_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('stats/', views.emotion_stats, name='emotion_stats'),
]