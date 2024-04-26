from django.db import models
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    data_publikacji = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)


