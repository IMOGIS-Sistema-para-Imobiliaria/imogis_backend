from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/", views.ReadCreateUserView.as_view()),
    path("users/<uuid:pk>/", views.RetrieveUpdateDeleteUserView.as_view()),
    path(
        "login/",
        TokenObtainPairView.as_view(),
    ),
]
