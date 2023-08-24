from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView

from .serialzers import UserLoginSerializers


class UserLoginAPIView(APIView):

    def post(self, request):
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user:
                auth.login(request=request, user=user)
                return Response(status=200)
            return Response(status=500)
        return Response(status=500)


class UserLogoutAPIView(APIView):

    def get(self, request):
        auth.logout(request=request)
        return Response(status=200)


