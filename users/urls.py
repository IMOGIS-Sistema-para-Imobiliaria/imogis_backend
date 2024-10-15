from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("accounts/", views.ReadCreateUserView.as_view()),
    path("accounts/<int:pk>", views.ReadCreateUserView.as_view()),
    path(
        "login/",
        TokenObtainPairView.as_view(),
    ),
]
