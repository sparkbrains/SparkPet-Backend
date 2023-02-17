from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.db import models
from django.conf import settings
import bcrypt



#custom user model

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by=models.CharField(max_length=250,null=True,blank=True)
    updated_by=models.CharField(max_length=250,null=True,blank=True)
    class Meta:
        abstract = True

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None):
        print('superuser')
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        print(user)
        user.is_admin = True
        user.save(using=self._db)
        return user        


class CustomUser(AbstractBaseUser,BaseModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = MyUserManager()
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin    

    def set_password(self, password):
        """
        Set the user's password to the given raw string, taking care to hash it
        first.
        """
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """
        Check the user's password against the given raw string.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))           

choice_here=(('dog','dog'),
           ('cat','cat') )       

class TypeChoices(models.TextChoices):
    DOG = "D", "DOG"
    CAT = "C", "CAT"

class GenderChoices(models.TextChoices):
        MALE = "M", "MALE"
        FEMALE = "F", "FEMALE"
    


class Profile(models.Model):

    '''
    PET PROFILE FIELDS 
    '''
    user  =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=250, null=True, blank=True)
    pet_name=models.CharField(max_length=250, null=True, blank=True)
    phone=models.IntegerField(null=True, blank=True)
    image=models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True, choices=GenderChoices.choices)
    type = models.CharField(max_length=255, null=True, blank=True, choices=TypeChoices.choices)
    breed=models.CharField(max_length=250, null=True, blank=True)
    height=models.CharField(max_length=250, null=True, blank=True)
    weight=models.CharField(max_length=250, null=True, blank=True)
    age=models.IntegerField(null=True, blank=True)