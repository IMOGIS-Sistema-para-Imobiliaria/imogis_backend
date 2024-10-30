from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from owners.models import Owner
from real_estate.models import RealEstate
from real_estate.serializers import RealEstateSerializer
from rest_framework.serializers import ValidationError


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

        if not owner_id:
            raise ValidationError("Owner ID is required.")

        owner = Owner.objects.filter(id=owner_id).first()

        if not owner:
            raise ValidationError("Invalid owner ID provided.")

        serializer.save(owner=owner)


class RetrieveUpdateDeleteRealEstateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer
