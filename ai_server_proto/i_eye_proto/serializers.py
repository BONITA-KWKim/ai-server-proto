from rest_framework import serializers
from .models import Checklist


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = ('reserved', 'created')
