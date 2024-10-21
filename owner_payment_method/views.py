from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from owner.models import Owner
from owner_payment_method.models import OwnerPaymentMethod
from owner_payment_method.serializers import OwnerPaymentMethodSerializer
from rest_framework.exceptions import NotFound


class ReadCreateOwnerPaymentMethodView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = OwnerPaymentMethod.objects.all()
    serializer_class = OwnerPaymentMethodSerializer

    def perform_create(self, serializer):
        owner_id_url = self.kwargs.get("owner_id")
        try:
            get_owner_id = Owner.objects.get(id=owner_id_url)
        except Owner.DoesNotExist:
            raise NotFound("Owner not found.")

        serializer.save(owner_id=get_owner_id)


class RetrieveUpdateDestroyOwnerPaymentMethodView(
    RetrieveUpdateDestroyAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = OwnerPaymentMethod.objects.all()
    serializer_class = OwnerPaymentMethodSerializer
