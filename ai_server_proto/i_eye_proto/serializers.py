from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Diagnosis, EyeImage


class UserSerializer(serializers.ModelSerializer):
    diagnosis = serializers.PrimaryKeyRelatedField(many=True, queryset=Diagnosis.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'checklist')


class DiagnosisSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Diagnosis
        fields = ('id', 'user_id', 'label', 'best_guess', 'web_entities', 'diagnosis', 'created', 'owner')


class EyeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = EyeImage
        fields = "__all__"
