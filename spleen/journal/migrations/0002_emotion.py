# Generated by Django 4.2.16 on 2024-09-11 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emotion', models.CharField(choices=[('😊', 'Happy'), ('😢', 'Sad'), ('😆', 'Laughing'), ('😐', 'Neutral'), ('😠', 'Angry')], max_length=1)),
                ('description', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emotions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
