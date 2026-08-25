from rest_framework import generics, permissions

from accounts.models import User
from accounts.serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    tags = ["auth"]


class MeView(generics.RetrieveUpdateAPIView):
    """Профиль текущего пользователя."""

    serializer_class = UserSerializer
    tags = ["auth"]

    def get_object(self):
        return self.request.user
