from django.db import models

# Create your models here.
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.CharField()
    project_pictures = models.ImageField()
    total_target = models.ImageField()
    tags = models.CharField()
    start_date = models.DateField()
    end_date = models.DateField()
    project_show=models.BooleanField(default=0)

class Images(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="media/projects/img")

