from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 
from . models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView
from rest_framework.exceptions import ValidationError



class UserRegistrationView(APIView):
    '''
    USER REGISTRATION VIEW AND ALSO CREATED THE PROFILE WHILE USER CREATED 
    '''
    def post(self, request, format=None):
        data=request.data
        #***ADD VALIDATION PASSWORD LENGTH
        if len(data.get('password'))<8:
            raise ValidationError('Password must be at least of 8 characters')
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user =serializer.save()
            parent_name=data.get("parent_name")
            pet_name=data.get("pet_name")
            phone=data.get("phone")
            breed=data.get("breed")
            height=data.get("height")
            weight=data.get("weight")
            gender=data.get("gender")
            age=data.get("age")
            Profile.objects.create(user=user,parent_name=parent_name,pet_name=pet_name,phone=phone,breed=breed,height=height,weight=weight,age=age)
            return Response('datasaved', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    '''
    USER LOGIN VIEW
    '''
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




class SendPasswordEmailView(APIView):
    '''
    SEND PASSWORD RESET EMAIL VIEW
    '''
    def post(self, request, formet=None):
        serializer = UserResetEmailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Password Reset link send. Please check your email"}, status=status.HTTP_200_OK)




class UserPasswordRestView(APIView):
    '''
    USER PASSWORD RESET VIEW
    '''
    def post(self, request, uid, token, formet=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Password Reset Successfully"}, status=status.HTTP_200_OK)






class ChangePasswordView(UpdateAPIView):

        """
        CHANGE PASSWORD VIEWS
        """

        serializer_class = ChangePasswordSerializer
        model = CustomUser
        permission_classes = (IsAuthenticated,)
        print('comes here')

        def get_object(self,queryset=None):
            obj = self.request.user
            print('comes up to get request')
            return obj
        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                #*** Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

                #*** set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

