from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.ReadCreateUserView.as_view()),
    path("users/<uuid:pk>/", views.RetrieveUpdateDeleteUserView.as_view()),
    path("login/", views.LastTokenObtainPairView.as_view()),
]
