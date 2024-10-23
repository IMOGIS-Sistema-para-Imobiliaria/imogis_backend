from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from client_payment_method.models import ClientPaymentMethod
from client_payment_method.serializers import ClientPaymentMethodSerializer
from rest_framework.serializers import ValidationError
from client_bank_details.models import ClientBankDetails
from client_pix_details.models import ClientPixDetails


class ReadCreateClientPaymentMethodView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ClientPaymentMethod.objects.all()
    serializer_class = ClientPaymentMethodSerializer

    def perform_create(self, serializer: ClientPaymentMethodSerializer):
        client_id: str = self.kwargs["client_id"]

        if client_id is None:
            raise ValidationError("Client ID is required.")

        existing_payment_method: list[ClientPaymentMethod] = (
            ClientPaymentMethod.objects.filter(client_id=client_id)
        )

        if existing_payment_method.exists():
            return Response(
                ClientPaymentMethodSerializer(
                    existing_payment_method.first()
                ).data,
                status=status.HTTP_200_OK,
            )

        serializer.save(client_id=client_id)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RetrieveUpdateDestroyClientPaymentMethodView(
    RetrieveUpdateDestroyAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ClientPaymentMethod.objects.all()
    serializer_class = ClientPaymentMethodSerializer

    def perform_update(self, serializer: ClientPaymentMethodSerializer):
        client_payment_method: ClientPaymentMethod = self.get_object()
        client_id: str = client_payment_method.client.id

        serializer.save(client_id=client_id)

        bank_details_data: list[dict[str, str]] = self.request.data.get(
            "bank_details", []
        )
        pix_details_data: list[dict[str, str]] = self.request.data.get(
            "pix_details", []
        )

        for bank_detail in bank_details_data:
            existing_bank_detail: ClientBankDetails = (
                ClientBankDetails.objects.filter(
                    client_payment_method=client_payment_method,
                    bank=bank_detail.get("bank"),
                    account=bank_detail.get("account"),
                    agency=bank_detail.get("agency"),
                ).first()
            )

            if existing_bank_detail:
                for key, value in bank_detail.items():
                    setattr(existing_bank_detail, key, value)
                existing_bank_detail.save()
            else:
                ClientBankDetails.objects.create(
                    client_payment_method=client_payment_method, **bank_detail
                )

        for pix_detail in pix_details_data:
            existing_pix_detail: ClientPixDetails = (
                ClientPixDetails.objects.filter(
                    client_payment_method=client_payment_method,
                    pix_key=pix_detail.get("pix_key"),
                ).first()
            )

            if existing_pix_detail:
                for key, value in pix_detail.items():
                    setattr(existing_pix_detail, key, value)
                existing_pix_detail.save()
            else:
                ClientPixDetails.objects.create(
                    client_payment_method=client_payment_method, **pix_detail
                )
