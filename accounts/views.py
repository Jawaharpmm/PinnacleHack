from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
#from rest_framework.response import Response
from .models import CareTaker
from .serializers import CaretakerSerializer

class CareTakerListView(APIView):
        serializer_class = CaretakerSerializer

       # def get_queryset(self):
            #get user and week_number from GET request
        #    phno = self.request.GET['phno']
         #   ctn = self.request.GET['ctn']
          #  cte = self.request.GET['cte']
          #  ctp = self.request.GET['ctp']
           # content = {'no':phno,'ctn':ctn,'cte':cte,'ctp':ctp}
           # return Response(content)
            #filter and return the first result where user=user and week=week
            #return Timesheet.objects.filter(user=user, week_number=week_number)
        def get(self, request):
                content = {'message': 'Hello, World!'}
                return Response(content)
        def post(self,request):
                #print(request.data)
                serializer = CaretakerSerializer(data=request.data)
                if serializer.is_valid():
                            
                            #print(request.data['us_name'])
                            #print(serializer.data['us_name'])
                            na = serializer.data['us_name']
                            #print(na)
                            us = User.objects.get(username=na)
                            #us = User()
                            #users = us.objects.all()
                            #print(us.email)
                            #ns = serializer.data['us_name']
                            #print(us)
                            ct = CareTaker(user=us,us_name=serializer.data['us_name'],phone_number=serializer.data['phone_number'], care_taker_name=serializer.data['care_taker_name'],care_taker_email=serializer.data['care_taker_email'],care_taker_no=serializer.data['care_taker_no'])
                            ct.save()
                            return Response(serializer.data)
                #return Response({'work':'done'})
                return Response(serializer.errors)