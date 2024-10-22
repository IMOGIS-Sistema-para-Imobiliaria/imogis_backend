from django.urls import path, include
from . import views

urlpatterns = [
    path(
        "users/",
        views.ReadCreateUserView.as_view(),
        name="user-list",
    ),
    path(
        "users/<uuid:pk>/",
        views.RetrieveUpdateDeleteUserView.as_view(),
        name="user-detail",
    ),
    path(
        "login/",
        views.LastTokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "users/password_reset/",
        include(
            "django_rest_passwordreset.urls",
            namespace="password_reset",
        ),
    ),
    path(
        "users/password_reset/code/",
        views.ResetPasswordConfirmView.as_view(),
        name="password-reset-code",
    ),
]
