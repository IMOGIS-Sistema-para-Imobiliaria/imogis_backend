from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from contracts.models import Contract
from contracts.serializers import ContractSerializer


class ReadCreateContractView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class RetrieveUpdateDeleteContractView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
