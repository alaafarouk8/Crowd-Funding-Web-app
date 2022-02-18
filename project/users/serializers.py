from rest_framework import serializers
from users.models import *

class usersSerializer(serializers.ModelSerializer):
    class Meta:
        model= Users
        fields = '__all__'
