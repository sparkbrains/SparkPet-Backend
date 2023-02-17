from django.urls import path
from .views import UserRegistrationView,LoginView,SendPasswordEmailView,UserPasswordRestView,ChangePasswordView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('send-password-reset-link/', SendPasswordEmailView.as_view(),name = "password-reset-email"),
    path('password-reset/<uid>/<token>/',UserPasswordRestView.as_view(), name = "password-reset"),
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),

]