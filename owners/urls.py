from django.urls import path
from . import views


urlpatterns = [
    path(
        "owners/",
        views.ReadCreateOwnerView.as_view(),
        name="owner-list",
    ),
    path(
        "owners/<uuid:pk>/",
        views.RetrieveUpdateOwnerView.as_view(),
        name="owner-detail",
    ),
    path(
        "owners/<uuid:pk>/delete/",
        views.DeleteOwnerView.as_view(),
        name="owner-delete",
    ),
]
