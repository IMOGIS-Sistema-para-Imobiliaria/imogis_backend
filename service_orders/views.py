from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from owners.models import Owner
from service_orders.models import ServiceOrder
from service_orders.serializers import ServiceOrderSerializer


class ReadCreateServiceOrderView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer

    def get_queryset(self):
        owner_id = self.kwargs["owner_id"]
        return ServiceOrder.objects.filter(owner_id=owner_id)

    def perform_create(self, serializer):
        owner_id = self.kwargs.get("owner_id")

        if not owner_id:
            raise ValidationError("Owner ID is required.")

        owner = Owner.objects.filter(id=owner_id).first()

        if not owner:
            raise ValidationError("Invalid owner ID provided.")

        serializer.save(owner=owner)


class RetrieveUpdateDestroyServiceOrderView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
