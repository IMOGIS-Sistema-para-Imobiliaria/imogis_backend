from django.urls import path
from . import views

urlpatterns = [
    path(
        "contracts/",
        views.ReadCreateContractView.as_view(),
        name="contracts-list",
    ),
    path(
        "contracts/<uuid:pk>/",
        views.RetrieveUpdateDeleteContractView.as_view(),
        name="contracts-detail",
    ),
]
