from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    class Type(models.TextChoices):
        DRAFT = 'seller', 'Seller'
        PUBLISHED = 'user', 'User'
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)
    user_type = models.CharField(max_length=10,choices=Type.choices,default=Type.DRAFT)

    def __str__(self):
        return f'Profile of {self.user.username}'