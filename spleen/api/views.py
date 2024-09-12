from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from journal.models import Emotion
from .serializers import UserSerializer, EmotionSerializer
from rest_framework.reverse import reverse

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register': reverse('register', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'create_emotion': reverse('create_emotion', request=request, format=format),
    })

@api_view(['POST'])
def login_view(request):
    serializer = ObtainAuthToken().post(request)
    return Response(serializer.data)

class EmotionCreateView(generics.CreateAPIView):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)