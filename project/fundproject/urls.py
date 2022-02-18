from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('/', views.home, name="home"),
    path('/createproject', views.create_project, name="create_project"),
    path('/project_list', views.list_project, name="list_project"),
    path('/projectlist/<id>', views.project_list, name="project_list"),
    path('/project/search/', views.search, name="search"),
    path('/project_info/<id>', views.project_info, name='project_info'),
    path('/comments/<id>', views.add_comment, name='comments'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


