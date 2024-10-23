from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from users.models import User
from users.permissions import IsSuperUserOrOwner
from users.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from rest_framework.views import status, APIView, Request, Response


class ReadCreateUserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveUpdateDeleteUserView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUserOrOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class LastTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args: list, **kwargs: dict):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(APIView):
    def post(self, request: Request, *args: list, **kwargs: dict):
        reset_code = request.data.get("reset_code")
        new_password = request.data.get("new_password")
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)

            if user.is_reset_code_valid(reset_code):
                user.set_password(new_password)
                user.reset_code = None
                user.reset_code_expires_at = None
                user.save()

                return Response(
                    {"message": "Password reset successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid or expired code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
