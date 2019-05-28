from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import Checklist
from .serializers import CheckListSerializer

# Create your views here.


@api_view(['GET'])
def index(request):
    return HttpResponse("Hello, world. You're at the IEyeProto index.")


@api_view(['GET'])
def version_info(request):
    return HttpResponse("V0.1.0 Prototype version")


class CheckList(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = CheckListSerializer


class CheckListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = CheckListSerializer

