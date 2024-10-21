from django.urls import path
from . import views


urlpatterns = [
    path(
        "<uuid:owner_id>/payment_method/",
        views.ReadCreateOwnerPaymentMethodView.as_view(),
        name="owner-payment_method-list",
    ),
    path(
        "<uuid:owner_id>/payment_method/<uuid:pk>/",
        views.RetrieveUpdateDestroyOwnerPaymentMethodView.as_view(),
        name="owner-payment_method-detail",
    ),
]
