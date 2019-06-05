from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Checklist


class CheckListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Checklist
        fields = ('id', 'owner', 'reserved', 'created')


class UserSerializer(serializers.ModelSerializer):
    checklist = serializers.PrimaryKeyRelatedField(many=True, queryset=Checklist.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'checklist')
