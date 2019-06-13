from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.decorators import api_view, action, detail_route
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from django.http import Http404

from .models import Diagnosis, EyeImage
from .serializers import UserSerializer, DiagnosisSerializer, EyeImageSerializer

import io
import os
# imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


# Create your views here.
@api_view(['GET'])
def index(request):
    test_google_vision()
    return HttpResponse("Hello, world. You're at the IEyeProto index.")


@api_view(['GET'])
def version_info(request):
    return HttpResponse("V0.1.0 Prototype version")


def get_permissions(self):
    if self.action == 'list':
        permission_classes = [AllowAny, ]
    else:
        permission_classes = [AllowAny, ]
    return [permission() for permission in permission_classes]


def test_google_vision():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(os.path.dirname(__file__), 'resources/faulkner.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    #response = client.object_localization(image=image)
    #labels = response.localized_object_annotations

    print('Labels: ')
    for label in labels:
        print('desc: ' + label.description + ', score: %.3f' % label.score)
    '''
    temp = 'desc: ' + labels[0].description + ', score: %.3f' % labels[0].score
    cl = Checklist(reserved=temp)
    cl.save()
    '''


'''
User
'''


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


'''
diagnosis test
'''


class DiagnosisList(generics.ListCreateAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.AllowAny, ]

    def list(self, request):
        print("diagnosis get method")
        queryset = self.get_queryset()
        serializer = DiagnosisSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print("diagnosis post method")

        file_serializer = EyeImageSerializer(data=request.FILES)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response("Success for saving the image")
        else:
            return Response("post")


class DiagnosisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.AllowAny, ]


class EyeImageList(generics.ListCreateAPIView):
    queryset = EyeImage.objects.all()
    serializer_class = EyeImageSerializer
    permission_classes = [permissions.AllowAny, ]
