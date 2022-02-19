from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

# app_name = 'fundproject'
urlpatterns = [
  #  path('/', views.home, name="home"),
    path('/create', views.create_project, name="create_project"),
    path('/project_list', views.list_project, name="list_project"),
    path('/projectlist/<id>', views.project_list, name="project_list"),
    path('/project_info/<id>', views.project_info, name='project_info'),
    path('/comments/<id>', views.add_comment, name='comments'),
    path('/cancel/<id>', views.cancel_project, name='cancel_project'),
    path('/report_project/<id>', views.report_project, name='report_project'),
    path('/search', views.search, name='search'),
    path('/report_comment/<id>', views.report_comment , name='report_comment' ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
