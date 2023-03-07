from django.urls import path,include
from .views import UserRegistrationView,LoginView,SendPasswordEmailView,UserPasswordRestView,ChangePasswordViews,ProfileView,PetProfileViews
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'update-profile', ProfileView)
router.register(r'petprofile',PetProfileViews)
# router.register(r'pet-profile-update',PetProfileUpdateViewset)
 

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/',LoginView.as_view(),name='login'),
    path('send-password-reset-link/', SendPasswordEmailView.as_view(),name = "password-reset-email"),
    path('password-reset/<uid>/<token>/',UserPasswordRestView.as_view(), name = "password-reset"),
    path('change-password/',ChangePasswordViews.as_view(),name='change_password'),
    # path('petprofileupdate/',PetProfileUpdateViewset.as_view(),name='petprofile'),
    # path('petprofile/',PetProfileViews.as_view(),name='PetProfileView'),

    path(r'', include(router.urls))
]