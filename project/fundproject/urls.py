from django.urls import path, include
from fundproject.views import *
urlpatterns = [
    path('',home, name = 'home'),

]
