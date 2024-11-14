from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from clients.models import Client
from property_invoices.models import PropertyInvoice
from property_invoices.serializers import PropertyInvoiceSerializer
from real_estate.models import RealEstate
from rest_framework.views import Response
from django.shortcuts import get_object_or_404


class ReadCreatePropertyInvoiceView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PropertyInvoice.objects.all()
    serializer_class = PropertyInvoiceSerializer

    def get_queryset(self):
        client_id = self.kwargs["client_id"]
        return PropertyInvoice.objects.filter(client_id=client_id)

    def perform_create(self, serializer):
        client_id = self.kwargs.get("client_id")
        real_estate_id = self.request.data.get("real_estate")

        real_estate_instance = None
        client_instance = None

        if real_estate_id:
            real_estate_instance = get_object_or_404(
                RealEstate, id=real_estate_id
            )

        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)

        serializer.save(
            real_estate=real_estate_instance, client=client_instance
        )


class RetrieveUpdateDeletePropertyInvoiceView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PropertyInvoice.objects.all()
    serializer_class = PropertyInvoiceSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)

        real_estate_id = request.data.get("real_estate")
        client_id = kwargs.get("client_id")

        real_estate_instance = None
        client_instance = None

        if real_estate_id:
            real_estate_instance = get_object_or_404(
                RealEstate, id=real_estate_id
            )
            serializer.validated_data["real_estate"] = real_estate_instance

        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)
            serializer.validated_data["client"] = client_instance

        serializer.save()
        return Response(serializer.data)
