from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from clients.models import Client
from property_invoices.models import PropertyInvoice
from property_invoices.serializers import PropertyInvoiceSerializer


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

        if not client_id:
            raise ValidationError("Client ID is required.")

        client = Client.objects.filter(id=client_id).first()

        if not client:
            raise ValidationError("Invalid client ID provided.")

        serializer.save(client=client)


class RetrieveUpdateDeletePropertyInvoiceView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PropertyInvoice.objects.all()
    serializer_class = PropertyInvoiceSerializer
