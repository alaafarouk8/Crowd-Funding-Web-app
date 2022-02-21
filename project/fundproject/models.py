from django.db import models
from users.models import Users

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
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


class Images (models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    img = models.ImageField(blank=False, null=False, upload_to='project')


class Tags (models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=40)


class Donation(models.Model):
    donation_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    donation_value = models.IntegerField()


class Rate(models.Model):
    rate_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    rate = models.IntegerField()


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.TextField(default='')


class CommentReports(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)



class ProjectReports(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)





        


