from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from clients.models import Client
from clients.permissions import IsSuperUserOrUserClient
from clients.serializers import ClientSerializer
from rest_framework.views import Response
from owners.models import Owner
from django.shortcuts import get_object_or_404


class ReadCreateClientView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        owner_id = self.request.data.get("owner")
        user = self.request.user

        if owner_id:
            owner_instance = get_object_or_404(Owner, id=owner_id)
            serializer.save(owner=owner_instance, user=user)
        else:
            serializer.save(user=user)


class RetrieveUpdateClientView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()

        owner_id = request.data.get("owner")
        user = request.user

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)

        if owner_id:
            owner_instance = get_object_or_404(Owner, id=owner_id)
            serializer.save(owner=owner_instance, user=user)
        else:
            serializer.save(user=user)

        return Response(serializer.data)


class DeleteClientView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUserOrUserClient]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
