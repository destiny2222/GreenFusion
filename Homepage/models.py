from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class SilderSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image = models.FileField()

    def __str__(self):
        return self.title

class AboutSection(models.Model):
    heading = models.CharField(max_length=200)
    body = RichTextField()  

    def __str__(self):
        return self.heading     