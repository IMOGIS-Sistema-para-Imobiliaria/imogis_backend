from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from bank_details.models import BankDetails
from bank_details.serializers import BankDetailsSerializer


class ReadCreateBankDetails(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BankDetails
    serializer_class = BankDetailsSerializer


class RetrieveUpdateDestroyBankDetails(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BankDetails
    serializer_class = BankDetailsSerializer
