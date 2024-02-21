from rest_framework import serializers
from .models import *
from users.serializers import userSerializer
from users.models import User
class noteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


class changeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change
        fields = '__all__'

