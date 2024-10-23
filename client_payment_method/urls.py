from django.urls import path
from . import views

urlpatterns = [
    path(
        "<uuid:client_id>/client_payment_method/",
        views.ReadCreateClientPaymentMethodView.as_view(),
        name="client_payment_method_list",
    ),
    path(
        "<uuid:client_id>/client_payment_method/<uuid:pk>/",
        views.RetrieveUpdateDestroyClientPaymentMethodView.as_view(),
        name="client_payment_method_detail",
    ),
]
