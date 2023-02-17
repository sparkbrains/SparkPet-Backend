from django.contrib import admin
from . models import CustomUser,Profile

# Register your models here.
admin.site.register(CustomUser)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','parent_name', 'pet_name','phone','image','gender','type','breed','height','weight','age')
