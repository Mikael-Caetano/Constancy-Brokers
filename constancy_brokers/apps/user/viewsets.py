from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from rest_framework import status, generics
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    serializer = UserSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        return Response(
            {"message": "Registration sucessfully completed."},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        token = Token.objects.get(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
