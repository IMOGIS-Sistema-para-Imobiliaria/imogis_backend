from django.urls import path
from . import views


urlpatterns = [
    path(
        "owner/",
        views.ReadCreateOwnerView.as_view(),
        name="owner-list",
    ),
    path(
        "owner/<uuid:pk>/",
        views.RetrieveUpdateOwnerView.as_view(),
        name="owner-detail",
    ),
    path(
        "owner/<uuid:pk>/delete/",
        views.DeleteOwnerView.as_view(),
        name="owner-delete",
    ),
]
