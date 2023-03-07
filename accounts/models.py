from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
from phonenumber_field.modelfields import PhoneNumberField



#custom user model


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
            print('heremodel')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        # user.is_staff = True
        # user.set_password(password)
        user.save(using=self._db)
        return user        


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
    objects = MyUserManager()
    def __str__(self):
        return self.email
  
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin    



class UserProfile(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_email')
    parent_name=models.CharField(max_length=255,null=True, blank= True)
    phone=PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.user.email




    
class PetGenderChoices(models.TextChoices):
    '''
    GENDER OF PET
    '''
    MALE = "M", "MALE"
    FEMALE = "F", "FEMALE"
    

class PetBreed(models.Model):
    pet_breed=models.CharField(max_length=255)

    def __str__(self):
        return self.pet_breed
    


class PetType(models.Model):
    pet_type=models.CharField(max_length=255) 
    breed_type=models.ForeignKey(PetBreed,on_delete=models.CASCADE,related_name='petbreed') 

    def __str__(self):
        return self.pet_type



    # def __str__(self):
    #     return self.image

    
class PetProfile(models.Model):
    '''
    PET PROFILE MODEL
    '''    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_name')
    pet_name=models.CharField(max_length=250,null=True)
    pet_age=models.CharField(max_length=250,null=True)
    pet_gender=models.CharField(max_length=250,null=True, blank=True, choices=PetGenderChoices.choices)
    breed=models.ForeignKey(PetBreed,on_delete=models.CASCADE,related_name='breedname')
    pet_type=models.ForeignKey(PetType,on_delete=models.CASCADE,related_name='breedtype')
    height=models.CharField(max_length=250, null=True, blank=True)
    weight=models.CharField(max_length=250, null=True, blank=True)


    

class Image(models.Model):
    pet_profile=models.ForeignKey(PetProfile,on_delete=models.CASCADE,related_name='petprofile')
    image=models.ImageField(upload_to='images/', max_length=254)