from django.urls import path
from . import views
urlpatterns = [

     path('', views.register , name='register'),
     path('/test', views.test , name='test')
]