from django.contrib import admin
from . models import CustomUser,UserProfile,PetProfile,PetBreed,PetType,Image

# Register your models here.



class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')

admin.site.register(CustomUser,UserAdmin)



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_name')

admin.site.register(UserProfile,ProfileAdmin)


class PetProfileAdmin(admin.ModelAdmin):
    list_display=('id','pet_name','pet_age','pet_gender','pet_breed','pet_type','weight','height')

    def pet_type(self,obj):
        return obj.pettype.pet_type

    def  pet_breed(self,obj):
        return obj.breed.pet_breed

    # def petimages(self,obj):
    #     return obj.petimage.image  

admin.site.register(PetProfile,PetProfileAdmin)

class PetBreedAdmin(admin.ModelAdmin):
    list_display=['pet_breed']

 

admin.site.register(PetBreed,PetBreedAdmin)


class PetTypeAdmin(admin.ModelAdmin):
    list_display=('pet_type','Breed_type')

    def Breed_type(self,obj):
        return obj.breed_type.pet_breed

admin.site.register(PetType,PetTypeAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display=('id','image')

admin.site.register(Image,ImageAdmin)   

