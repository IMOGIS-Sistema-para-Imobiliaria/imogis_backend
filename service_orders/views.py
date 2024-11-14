from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from owners.models import Owner
from real_estate.models import RealEstate
from service_orders.models import ServiceOrder
from service_orders.serializers import ServiceOrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import Response


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
        real_estate_id = self.request.data.get("real_estate")

        owner_instance = None
        real_estate_instance = None

        if owner_id:
            owner_instance = get_object_or_404(Owner, id=owner_id)

        if real_estate_id:
            real_estate_instance = get_object_or_404(
                RealEstate, id=real_estate_id
            )

        serializer.save(owner=owner_instance, real_estate=real_estate_instance)


class RetrieveUpdateDestroyServiceOrderView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)

        owner_id = self.kwargs.get("owner_id")
        real_estate_id = self.request.data.get("real_estate")

        real_estate_instance = None
        ownner_instance = None

        if owner_id:
            ownner_instance = get_object_or_404(Owner, id=owner_id)
            serializer.validated_data["owner"] = ownner_instance

        if real_estate_id:
            real_estate_instance = get_object_or_404(
                RealEstate, id=real_estate_id
            )
            serializer.validated_data["real_estate"] = real_estate_instance

        serializer.save()
        return Response(serializer.data)
