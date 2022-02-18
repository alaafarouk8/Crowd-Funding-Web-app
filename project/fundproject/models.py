from django.db import models

# Create your models here.


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    details = models.TextField()
    total_target = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)


class Images (models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    img = models.ImageField(blank=False, null=False, upload_to='project')


class Tags (models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=40)




        



