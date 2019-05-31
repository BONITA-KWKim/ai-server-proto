from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import Checklist
from .serializers import CheckListSerializer

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


class CheckList(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = CheckListSerializer


class CheckListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = CheckListSerializer


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
