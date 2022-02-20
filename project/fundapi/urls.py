from django.urls import include, path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'projectListView' , projectListView)


urlpatterns = [
    path('', include(router.urls)),
   # path('' , views.test , name='test' )
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]