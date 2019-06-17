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

from .forms import ImageUploadForm
from .models import Diagnosis, EyeImage
from .serializers import UserSerializer, DiagnosisSerializer, EyeImageSerializer
from .custom_utils.whitelist_for_labels import get_whitelist_value, get_refusal_value, get_whitelist_score_value
from .custom_utils.eye_disease import get_disease_value, get_disease_score_value

import io
import os
# imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


# Create your views here.
@api_view(['GET'])
def index(request):
    print(get_whitelist_value("f"))
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


import base64
def get_google_vision_response(photo):
    print("[DEB] get google vision response")
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    content = photo['eye_photo'].read()
    '''
    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations # annotate_image({"":""})

    print('Labels: ')
    for label in labels:
        print('desc: ' + label.description + ', score: %.3f' % label.score)
    '''

    response = client.annotate_image(
        {
            "image": {
                "content": content
            },
            "features": [
                {
                    "type": vision.enums.Feature.Type.SAFE_SEARCH_DETECTION
                },
                {
                    "type": vision.enums.Feature.Type.LABEL_DETECTION
                },
                {
                    "type": vision.enums.Feature.Type.WEB_DETECTION
                }
            ],
        }
    )

    return response


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
        queryset = self.get_queryset()

        # get a file and check
        file_serializer = EyeImageSerializer(data=request.data)

        if file_serializer.is_valid():
            response = get_google_vision_response(request.FILES)
            '''
            save search result
            1: VERY_UNLIKELY
            2: UNLIKELY
            3: POSSIBLE
            4: LIKELY
            5: VERY_LIKELY
            '''
            # 1. check safe search
            print("========== safe search ==========")
            safe_search = response.safe_search_annotation
            if 5 == safe_search.racy or 5 == safe_search.adult:
                return Response("Safe search", status=status.HTTP_400_BAD_REQUEST)

            # 2. recognize human eyes
            # white list with index
            # create parsing json module referenced by conf.custom_utils
            # Upper case to lower case
            print("========== label annotations ==========")
            labels = response.label_annotations
            label_score = 0
            for l in labels:
                print("[DEB] desc:", l.description)
                first_char = l.description[0]
                print("[DEB]first character: %c" % first_char)
                whitelist_by_index = get_whitelist_value(first_char.lower())
                refusal_list_by_index = get_refusal_value(first_char.lower())
                print("[DEB]whitelist: ", whitelist_by_index)
                print("[DEB]refusal: ", refusal_list_by_index)

                for s in whitelist_by_index:
                    print("[DEB] s value: ", s)
                    print("[DEB] match: ", l.description.lower() == s)

                if l.description.lower() in whitelist_by_index:
                    print("[DEB] match the white list")
                    print(l.description.lower())
                    print(whitelist_by_index)
                    label_score += 1

                if any(l.description.lower() is s for s in refusal_list_by_index):
                    print("[DEB] refusal")
                    print(l.description.lower())
                    print(refusal_list_by_index)
                    return Response("Bad image", status=status.HTTP_400_BAD_REQUEST)

            if get_whitelist_score_value() > label_score:
                print("[DEB] not enough score: %d" % label_score)
                return Response("Bad image", status=status.HTTP_400_BAD_REQUEST)

            print("[DEB] score value: ", label_score)

            # 3. What state is the eyes
            print("========== web detections ==========")
            web_detections = response.web_detection
            best_guess = web_detections.best_guess_labels
            web_entities = web_detections.web_entities
            print("[DEB] best guess: ", best_guess)
            print("[DEB] web entities: ", web_entities)

            # 3.1. best guess
            for b in best_guess:
                first_char = b.label[0]
                disease_list_by_index = get_disease_value(first_char.lower())
                if b.label.lower() in disease_list_by_index:
                    print("Success: Disease[%s]" % b.label.lower())
                    #return Response("Success: Disease[%s]" % b.label.lower(), status=status.HTTP_201_CREATED)

            # 3.2. web entities
            for w in web_entities:
                print("[DEB] desc: ", w.description)
                print("[DEB] score: ", w.score)
                first_char = w.description[0]
                disease_list_by_index = get_disease_value(first_char.lower())

                if w.description.lower() in disease_list_by_index:
                    print("Success: Disease[%s]" % w.description.lower())
                    #return Response("Success disease: %s" % w.description.lower(), status=status.HTTP_201_CREATED)

            print("[DEB] end of the image analysis")
            # save results into database
            # file_serializer.save()
            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            return Response("Failure", status=status.HTTP_400_BAD_REQUEST)


class DiagnosisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.AllowAny, ]


class EyeImageList(generics.ListAPIView):
    queryset = EyeImage.objects.all()
    serializer_class = EyeImageSerializer
    permission_classes = [permissions.AllowAny, ]

