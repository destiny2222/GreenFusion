# from django.db import models
# from django.contrib.auth.models import User,AbstractUser
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _

# # Create your models here.


# class  CustomUser(AbstractUser):
#     fullname = models.CharField(max_length=20)
#     username = models.CharField(max_length=20,unique=True)
#     number = models.CharField(max_length=11, blank=True)
#     description = models.TextField()
#     about = models.TextField( max_length=250)
#     level = models.CharField(max_length=20)
#     gender = models.CharField(max_length=20)
#     photo = models.FileField(default='avatar.png', upload_to='profile_img')
   
    


#     def __str__(self):
#         return self.username 



