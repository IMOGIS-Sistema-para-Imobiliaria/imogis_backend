from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from pix_details.models import PixDetails
from pix_details.serializers import PixDetailsSerializer


class ReadCreatePixDetails(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PixDetails
    serializer_class = PixDetailsSerializer


class RetrieveUpdateDestroyPixDetails(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PixDetails
    serializer_class = PixDetailsSerializer
