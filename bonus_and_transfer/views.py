from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from bonus_and_transfer.models import BonusAndTransfer
from bonus_and_transfer.serializers import BonusAndTransferSerializer


class ReadCreateBonusAndTransfer(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BonusAndTransfer
    serializer_class = BonusAndTransferSerializer


class RetrieveUpdateDestroyBonusAndTransfer(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = BonusAndTransfer
    serializer_class = BonusAndTransferSerializer
