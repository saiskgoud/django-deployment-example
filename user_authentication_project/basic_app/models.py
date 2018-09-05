from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):

    #create relationship (don't inherit from User)
    user=models.OneToOneField(User)

    #additional attributes
    portfolio_site=models.URLField(blank=True)
    #blank=True is used it is not mandatory

    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username