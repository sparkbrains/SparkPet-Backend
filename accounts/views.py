from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated 
from . models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated   
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView
from django.http import HttpResponse


#registration view
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = User(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            phone = request.data['phone']
            parent_name = request.data['parent_name']
            profile=UserProfile.objects.create(user=user,parent_name=parent_name,phone=phone)
        else:
            return Response(serializer.errors)
        return Response('data saved')

    # def get(self,request):
    #     profile=UserProfile.objects.all()
    #     serializer = UserProfileSerializer(profile,many=True)
    #     return Response(serializer.data)
# queryset = PetProfile.objects.all()


#login view
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        return Response(
            {'refresh':  str(refresh),
            'access': str(refresh.access_token),
            'data':serializer.data
            } 
            )    



#reset password
class SendPasswordEmailView(APIView):
    def post(self, request, formet=None):
        serializer = UserResetEmailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Password Reset link send. Please check your email"}, status=status.HTTP_200_OK)


class UserPasswordRestView(APIView):
    def post(self, request, uid, token, formet=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Password Reset Successfully"}, status=status.HTTP_200_OK)
queryset = PetProfile.objects.all()



class ChangePasswordViews(APIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            confirm_password = serializer.data.get('confirm_new_password')
            if new_password != confirm_password :
                return Response({'message': 'New password and confirm password does not match.'}, status=status.HTTP_400_BAD_REQUEST)
            elif len(new_password)<8:
                return Response({'message': 'minimum length of password more than 8'}, status=status.HTTP_400_BAD_REQUEST)    
            user = CustomUser.objects.get(email=request.user.email)
            if user:
                if user.check_password(old_password)==True:
                    if old_password==new_password:
                        return Response({'message': 'Password already has been used by you previous time please enter new password'}, status=status.HTTP_400_BAD_REQUEST)   
                    user.set_password(new_password)
    
                    user.save()
                    
                    return Response({'message': 'Password successfully updated.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'old password you entered is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(viewsets.ModelViewSet):
    serializer_class=UpdateUserProfileSerializer
    queryset = UserProfile.objects.all()
    def update(self, request, *args, **kwargs):
        partial=True
        instance = self.get_object()
        serializer=self.get_serializer(instance,data=request.data,partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class PetProfileViews(viewsets.ModelViewSet):
    serializer_class=PetProfileSerializer
    queryset = PetProfile.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    '''
    Update View
    '''
    def update(self,request,*args,**kwargs):
        partial=True
        instance=self.get_object()
        serializer=self.get_serializer(instance,data=request.data,partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)












        



