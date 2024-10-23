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

# from rest_framework.views import Response


class ReadCreateClientView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateClientView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    # def update(self, request, *args, **kwargs):
    #     partial = request.method == "PATCH"
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=partial
    #     )

    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)

    #     return Response(serializer.data)


class DeleteClientView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUserOrUserClient]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
