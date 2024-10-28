from django.urls import path
from . import views

urlpatterns = [
    path(
        "<uuid:owner_id>/service_orders/",
        views.ReadCreateServiceOrderView.as_view(),
        name="service_orders_list",
    ),
    path(
        "<uuid:owner_id>/service_orders/<uuid:pk>/",
        views.RetrieveUpdateDestroyServiceOrderView.as_view(),
        name="service_orders_detail",
    ),
]
