from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from owner_payment_method.models import OwnerPaymentMethod
from owner_payment_method.serializers import OwnerPaymentMethodSerializer
from rest_framework.views import Response, status
from rest_framework.serializers import ValidationError


class ReadCreateOwnerPaymentMethodView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = OwnerPaymentMethod.objects.all()
    serializer_class = OwnerPaymentMethodSerializer

    def perform_create(self, serializer: OwnerPaymentMethodSerializer):
        owner_id = self.kwargs["owner_id"]

        if owner_id is None:
            raise ValidationError("Owner ID is required.")

        existing_payment_method = OwnerPaymentMethod.objects.filter(
            owner_id=owner_id
        ).first()

        if existing_payment_method:
            return Response(
                self.get_serializer(existing_payment_method).data,
                status=status.HTTP_200_OK,
            )

        serializer.save(owner_id=owner_id)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RetrieveUpdateDestroyOwnerPaymentMethodView(
    RetrieveUpdateDestroyAPIView
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = OwnerPaymentMethod.objects.all()
    serializer_class = OwnerPaymentMethodSerializer

    def perform_update(self, serializer: OwnerPaymentMethodSerializer):
        instance = self.get_object()
        serializer.update(instance, self.request.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
