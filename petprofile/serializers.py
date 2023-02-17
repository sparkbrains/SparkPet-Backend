from rest_framework import serializers
from .models import CustomUser,Profile
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import smart_str,  force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _




class ProfileSerializer(serializers.ModelSerializer):
    '''
    USER PROFILE VIEW SERIALIZATION
    '''
    class Meta:
        model=Profile
        fields=('parent_name','pet_name','phone','image','gender', 'type', 'breed','height', 'weight','age')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    '''
    USER REGSITRATION SERIALIZATION
    '''
    class Meta:
        model=CustomUser
        fields = ( 'email','password')
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
            #    ***   CONFIRMATION EMAIL OF REGISTERED USER   ***
            # subject = 'Welcome to Our Site!'
            # message = 'Thank you for registering. We are happy to have you as a part of our community.'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = user
            # send_mail(subject, message, email_from, (recipient_list.email,))                   
        return user



#login serializers
class LoginSerializer(serializers.Serializer):
    '''
    LOGIN SERIALIZER
    '''
    email = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        email=data.get('email')
        password=data.get('password')
        if email and password:
            user = authenticate(email=email,password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")  



class UserResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    '''
    RESET PASSWORD EMAIL SEND SERIALIZATION
    '''
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email = attrs.get('email')
        user = CustomUser.objects.get(email=email)
        request = self.context.get('request')
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            #    ***  SEND RESET PASSWORD LINK ,UID AND TOKEN IN EMAIL   ***
            link = "http://127.0.0.1:8000/password-reset/" + uid + '/' + token
            subject = 'password reset email'
            message = 'TO RESET YOUR PASSWORD CLICK ON THE GIVEN LINK'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = user
            send_mail(subject, message +"  "+ link, email_from, (recipient_list.email,))        
        else:
            raise serializers.ValidationError('You are not a registred user')




class UserPasswordResetSerializer(serializers.Serializer):
    '''
    USER PASSWORD RESET SERIALIZER
    '''
    password = serializers.CharField(
        max_length=15, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=15, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            #***GENERATE PASSWORD RESET TOKEN 
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password are not same")
            user_id = smart_str(urlsafe_base64_decode(uid))
            try:
                user = CustomUser.objects.get(id=user_id)
            except Exception as e:
                return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not valid or Expired')
            #  ***  SET PASSWORD IS USED FOR HAS THE PASSWORD ***    
            user.set_password(password)
            user.save()            
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError('Token is not Valid or Expired')




class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    print('comes from')
