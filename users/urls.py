from django.urls import path, include
from . import views

urlpatterns = [
    path("users/", views.ReadCreateUserView.as_view()),
    path("users/<uuid:pk>/", views.RetrieveUpdateDeleteUserView.as_view()),
    path("login/", views.LastTokenObtainPairView.as_view()),
    path(
        "users/password_reset_code/", views.ResetPasswordConfirmView.as_view()
    ),
    path(
        "users/password_reset/",
        include(
            "django_rest_passwordreset.urls",
            namespace="password_reset",
        ),
    ),
]
