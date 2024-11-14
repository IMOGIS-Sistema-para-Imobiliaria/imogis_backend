from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from clients.models import Client
from owners.models import Owner
from real_estate.models import RealEstate
from real_estate.serializers import RealEstateSerializer
from rest_framework.serializers import ValidationError
from rest_framework.views import Response
from django.shortcuts import get_object_or_404


class ReadCreateRealEstateView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer

    def get_queryset(self):
        owner_id = self.kwargs["owner_id"]
        return RealEstate.objects.filter(owner_id=owner_id)

    def perform_create(self, serializer):
        owner_id = self.kwargs.get("owner_id")
        client_id = self.request.data.get("client")

        if not owner_id:
            raise ValidationError("Owner ID is required.")

        owner = Owner.objects.filter(id=owner_id).first()

        if not owner:
            raise ValidationError("Invalid owner ID provided.")

        client_instance = None
        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)
            serializer.save(owner=owner, client=client_instance)
        else:
            serializer.save(owner=owner, client=client_instance)


class RetrieveUpdateDeleteRealEstateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)

        client_id = request.data.get("client")
        user = request.user

        client_instance = None
        if client_id:
            client_instance = get_object_or_404(Client, id=client_id)
            serializer.validated_data["client"] = client_instance

        serializer.save(user=user)
        return Response(serializer.data)
