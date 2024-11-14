from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from bonus_and_transfer.models import BonusAndTransfer
from bonus_and_transfer.serializers import BonusAndTransferSerializer
from clients.models import Client
from owners.models import Owner
from django.shortcuts import get_object_or_404
from rest_framework.views import Response


class ReadCreateBonusAndTransfer(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BonusAndTransfer.objects.all()
    serializer_class = BonusAndTransferSerializer

    def perform_create(self, serializer):
        client_id = self.request.data.get("client")
        owner_id = self.request.data.get("owner")

        client_instance = None
        owner_instance = None

        if owner_instance:
            owner_instance = get_object_or_404(Owner, id=owner_id)

        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)

        serializer.save(owner=owner_instance, client=client_instance)


class RetrieveUpdateDestroyBonusAndTransfer(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BonusAndTransfer.objects.all()
    serializer_class = BonusAndTransferSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)

        owner_id = request.data.get("owner")
        client_id = request.data.get("client")

        owner_instance = None
        client_instance = None

        if owner_id:
            owner_instance = get_object_or_404(Owner, id=owner_id)
            serializer.validated_data["owner"] = owner_instance

        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)
            serializer.validated_data["client"] = client_instance

        serializer.save()
        return Response(serializer.data)
