import pandas as pd
import plotly.express as px
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, EmotionForm
from .models import JournalEntry, Emotion
from datetime import datetime, timedelta
from django.utils import timezone

# Функция для определения правильного формата времени и даты
def format_timestamp(timestamp):
    now = timezone.localtime()
    difference = now - timestamp

    if difference.days == 0:
        return f'Сегодня, {timestamp.strftime("%H:%M")}'
    elif difference.days == 1:
        return f'Вчера, {timestamp.strftime("%H:%M")}'
    elif difference.days == 2:
        return f'Позавчера, {timestamp.strftime("%H:%M")}'
    else:
        return timestamp.strftime('%d.%m.%Y, %H:%M')

# Группировка эмоций по дням
def group_emotions_by_day(emotions):
    grouped_emotions = {}
    today_str = timezone.localtime().strftime('%Y-%m-%d')
    yesterday_str = (timezone.localtime() - timedelta(1)).strftime('%Y-%m-%d')
    two_days_ago_str = (timezone.localtime() - timedelta(2)).strftime('%Y-%м-%d')

    for emotion in emotions:
        local_time = timezone.localtime(emotion.timestamp)
        day_str = local_time.strftime('%Y-%m-%d')
        
        if day_str not in grouped_emotions:
            grouped_emotions[day_str] = []
        
        formatted_timestamp = format_timestamp(local_time)
        emotion.formatted_timestamp = formatted_timestamp
        grouped_emotions[day_str].append(emotion)

    today = today_str
    yesterday = yesterday_str
    two_days_ago = two_days_ago_str

    return grouped_emotions, today, yesterday, two_days_ago

# Главная страница
def index(request):
    if request.user.is_authenticated:
        entries = Emotion.objects.filter(user=request.user).order_by('-timestamp')
        grouped_entries, today, yesterday, two_days_ago = group_emotions_by_day(entries)
        return render(request, 'journal/index.html', {
            'grouped_entries': grouped_entries,
            'today': today,
            'yesterday': yesterday,
            'two_days_ago': two_days_ago,
            'user_is_authenticated': True,
        })
    else:
        return render(request, 'journal/index.html', {'user_is_authenticated': False})


# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'journal/register.html', {'form': form})

# Вход
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'journal/login.html', {'form': form})

# Выход
def logout_view(request):
    logout(request)
    return redirect('index')

# Создание новой эмоции
@login_required
def emotion_create(request):
    if request.method == 'POST':
        form = EmotionForm(request.POST)
        if form.is_valid():
            emotion = form.save(commit=False)
            emotion.user = request.user
            emotion.save()
            return redirect('index')
    else:
        form = EmotionForm()
    return render(request, 'journal/emotion_form.html', {'form': form, 'is_new': True})

# Обновление эмоции
@login_required
def emotion_update(request, pk):
    emotion = get_object_or_404(Emotion, pk=pk)
    if request.method == 'POST':
        form = EmotionForm(request.POST, instance=emotion)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EmotionForm(instance=emotion)
    return render(request, 'journal/emotion_form.html', {'form': form, 'is_new': False})

# Удаление эмоции
@login_required
def emotion_delete(request, pk):
    emotion = get_object_or_404(Emotion, pk=pk)
    if request.method == 'POST':
        emotion.delete()
        return redirect('index')
    return render(request, 'journal/emotion_confirm_delete.html', {'emotion': emotion})

# Статистика эмоций
@login_required
def emotion_stats(request):
    emotions = Emotion.objects.filter(user=request.user).order_by('timestamp')
    
    # Подготовка данных для графика
    data = {
        'timestamp': [emotion.timestamp for emotion in emotions],
        'balance_change': [(1 if emotion.emotion == '😊' else
                           -1 if emotion.emotion == '😢' else
                            2 if emotion.emotion == '😆' else
                           -2 if emotion.emotion == '😠' else 0) for emotion in emotions]
    }

    df = pd.DataFrame(data)
    df['cumulative_balance'] = df['balance_change'].cumsum()

    # Создание графика
    fig = px.line(df, x='timestamp', y='cumulative_balance', labels={'timestamp': 'Дата', 'cumulative_balance': 'Эмоциональный баланс'}, title='Динамика эмоционального баланса')
    graph_html = fig.to_html(full_html=False)
    
    return render(request, 'journal/emotion_stats.html', {'graph_html': graph_html})