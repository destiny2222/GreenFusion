from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.



class About(models.Model):
    heading = models.CharField(max_length=200)
    body = RichTextField()
    image = models.FileField()

    def __str__(self):
        return self.heading