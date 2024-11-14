from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from clients.models import Client
from contracts.models import Contract
from contracts.serializers import ContractSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from owners.models import Owner
from real_estate.models import RealEstate


class ReadCreateContractView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def perform_create(self, serializer):
        client_id = self.request.data.get("client")
        owner_id = self.request.data.get("owner")
        real_estate_id = self.request.data.get("real_estate")

        client_instance = None
        owner_instance = None
        real_estate_instance = None

        if owner_id:
            owner_instance = get_object_or_404(Owner, id=owner_id)

        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)

        if real_estate_id:
            real_estate_instance = get_object_or_404(
                RealEstate, id=real_estate_id
            )

        serializer.save(
            owner=owner_instance,
            client=client_instance,
            real_estate=real_estate_instance,
        )


class RetrieveUpdateDeleteContractView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)

        client_id = request.data.get("client")
        owner_id = request.data.get("owner")
        real_estate_id = request.data.get("real_estate")

        client_instance = None
        owner_instance = None
        real_estate_instance = None

        if owner_id:
            owner_instance = get_object_or_404(Owner, id=owner_id)
            serializer.validated_data["owner"] = owner_instance

        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)
            serializer.validated_data["client"] = client_instance

        if real_estate_id:
            real_estate_instance = get_object_or_404(
                RealEstate, id=real_estate_id
            )
            serializer.validated_data["real_estate"] = real_estate_instance

        serializer.save()
        return Response(serializer.data)
