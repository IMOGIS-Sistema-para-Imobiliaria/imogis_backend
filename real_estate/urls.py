from django.urls import path
from . import views

urlpatterns = [
    path(
        "<uuid:owner_id>/real_estate/",
        views.ReadCreateRealEstateView.as_view(),
        name="real_estate-list",
    ),
    path(
        "<uuid:owner_id>/real_estate/<uuid:pk>/",
        views.RetrieveUpdateDeleteRealEstateView.as_view(),
        name="real_estate-detail",
    ),
]
