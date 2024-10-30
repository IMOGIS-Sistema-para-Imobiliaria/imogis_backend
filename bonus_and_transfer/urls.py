from django.urls import path
from . import views

urlpatterns = [
    path(
        "bonus_and_transfer/",
        views.ReadCreateBonusAndTransfer.as_view(),
        name="bonus_and_transfer_list",
    ),
    path(
        "bonus_and_transfer/<uuid:pk>/",
        views.RetrieveUpdateDestroyBonusAndTransfer.as_view(),
        name="bonus_and_transfer_detail",
    ),
]
