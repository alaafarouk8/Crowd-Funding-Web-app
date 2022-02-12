from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.CharField(choices=['children', 'Entrepreneurs', 'Medical', 'Technology'])
    project_pictures = models.ImageField()
    total_target = models.ImageField()
    tags = models.(choices=['children', 'Entrepreneurs', 'Medical', 'Technology'])
