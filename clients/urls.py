from django.urls import path
from . import views


urlpatterns = [
    path(
        "clients/",
        views.ReadCreateClientView.as_view(),
        name="client-list",
    ),
    path(
        "clients/<uuid:pk>/",
        views.RetrieveUpdateClientView.as_view(),
        name="client-detail",
    ),
    path(
        "clients/<uuid:pk>/delete/",
        views.DeleteClientView.as_view(),
        name="client-delete",
    ),
]
