from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)

from owners.models import Owner
from owners.permissions import IsSuperUserOrUserOwner
from owners.serializers import OwnerSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response


class ReadCreateOwnerView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateOwnerView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)


class DeleteOwnerView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUserOrUserOwner]

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
