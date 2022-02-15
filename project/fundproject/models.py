from django.db import models

# Create your models here.
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.CharField(max_length=100)
    project_pictures = models.ImageField()
    total_target = models.ImageField()
    tags = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    project_show=models.BooleanField(default=0)



