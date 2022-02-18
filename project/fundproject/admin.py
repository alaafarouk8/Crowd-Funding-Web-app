from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Categories)
admin.site.register(Project)
admin.site.register(Images)
admin.site.register(Tags)
admin.site.register(Comment)
admin.site.register(Donation)
admin.site.register(CommentReports)
admin.site.register(ProjectReports)
admin.site.register(Rate)