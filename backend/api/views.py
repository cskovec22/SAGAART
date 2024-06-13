from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status, views, viewsets

from api.serializers import CustomUserSerializer, LoginSerializer
from users.models import CustomUser


class CustomUserSetView(viewsets.ModelViewSet):
    """
    Вьюсет для создания, просмотра, редактирования и удаления пользователя.
    """
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserRegistrationView(views.APIView):
    """Представление для регистрации пользователя."""

    def post(self, request):
        """Регистрация пользователя."""
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    """Вход пользователя."""

    def post(self, request):
        """Вход пользователя по электронной почте и паролю."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Неверные учетные данные."},
            status=status.HTTP_401_UNAUTHORIZED
        )
