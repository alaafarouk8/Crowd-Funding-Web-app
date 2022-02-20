from django.shortcuts import render
from rest_framework import viewsets
from fundproject.models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view

# Create your views here.

class projectListView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

def test(request):
    return HttpResponse('hello')