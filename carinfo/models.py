from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Car(models.Model):
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='car_details')
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    model = models.TextField()
    year = models.IntegerField()
    price = models.IntegerField()
    location = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    #Default ordering and Indexing
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created']),]

    def __str__(self):
        return self.title

class Comment(models.Model):
    car = models.ForeignKey(Car,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)

    def __str__(self):
        return f'Image for {self.car}'