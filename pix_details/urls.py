from django.urls import path
from . import views

urlpatterns = [
    path(
        "pix_details/",
        views.ReadCreatePixDetails.as_view(),
        name="pix_details_list",
    ),
    path(
        "pix_details/<uuid:pk>/",
        views.RetrieveUpdateDestroyPixDetails.as_view(),
        name="pix_details_detail",
    ),
]
