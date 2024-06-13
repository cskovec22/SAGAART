from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from api.views import CustomUserSetView, LoginView, UserRegistrationView


url_token = [
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),

]

urlpatterns = [
    path(
        "registration/",
        UserRegistrationView.as_view(),
        name="registration"
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),
    path("token/", include(url_token)),
    # path("v1/", include("api.urls")),
]
