from django.urls import path
from . import views

urlpatterns = [
    path(
        "bank_details/",
        views.ReadCreateBankDetails.as_view(),
        name="bank_details_list",
    ),
    path(
        "bank_details/<uuid:pk>/",
        views.RetrieveUpdateDestroyBankDetails.as_view(),
        name="bank_details_detail",
    ),
]
