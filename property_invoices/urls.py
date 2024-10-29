from django.urls import path
from . import views

urlpatterns = [
    path(
        "<uuid:client_id>/property_invoices/",
        views.ReadCreatePropertyInvoiceView.as_view(),
        name="property_invoices-list",
    ),
    path(
        "<uuid:client_id>/property_invoices/<uuid:pk>/",
        views.RetrieveUpdateDeletePropertyInvoiceView.as_view(),
        name="property_invoices-detail",
    ),
]
