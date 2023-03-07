from rest_framework import serializers
from .models import CustomUser,UserProfile,PetProfile,Image
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import smart_str, smart_bytes, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.html import strip_tags
from rest_framework.response import Response

#registration serializers
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=('user','parent_name','phone',)

class User(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields = ( 'email','password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)                 
        return user

#login serializers
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")          


#reset password
class UserResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user = CustomUser.objects.get(email=email)
        request = self.context.get('request')
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://127.0.0.1:8000/password-reset/" + uid + '/' + token
            subject = 'password reset email'
            message = 'TO RESET YOUR PASSWORD CLICK ON THE GIVEN LINK'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = user
            print(recipient_list,'rrr')
            send_mail(subject, message +"  "+ link, email_from, (recipient_list.email,))
            return Response('ok')
        else:
            raise serializers.ValidationError('You are not a registred user')


       




class UserPasswordResetSerializer(serializers.Serializer):
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
            print(uid,'uid')
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
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError('Token is not Valid or Expired')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password=serializers.CharField(required=True)


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('parent_name', 'phone')
        extra_kwargs = {
            'parent_name': {'required': True},
            'phone': {'required': True},
        }


#personla code___

class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Image
        fields=["image"]

class PetProfileSerializer(serializers.ModelSerializer):
    upload_images=serializers.ListField(
    child=serializers.ImageField(max_length=100000,allow_empty_file=False,use_url=False),write_only=True
    )
    class Meta:
        model=PetProfile
        fields=('user','pet_name','pet_age','upload_images','pet_gender','breed','pet_type','height','weight')

    def create(self,validate_data):
        uploaded_images = validate_data.pop("upload_images")
        petname=PetProfile.objects.create(**validate_data)

        for image in uploaded_images:
            pet_images=Image.objects.create(pet_profile=petname,image=image)
        return petname





