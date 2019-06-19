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

# imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

import logging

# Create your views here.
logger = logging.getLogger('ai_server_proto.i_eye_proto')


@api_view(['GET'])
def index(request):
    logger.debug("test!!")
    logger.info("information test !!")
    return HttpResponse("Hello, world. You're at the IEyeProto index.")


@api_view(['GET'])
def version_info(request):
    return HttpResponse("V0.1.0 Prototype version")


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
        # return Response(serializer.data["diagnosis"])
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print("[DEB] diagnosis post method")
        # get a file and check
        file_serializer = EyeImageSerializer(data=request.data)

        if file_serializer.is_valid():
            response = get_google_vision_response(request.FILES)
            '''
            1. check safe search
              - save search result
               1: VERY_UNLIKELY
               2: UNLIKELY
               3: POSSIBLE
               4: LIKELY
               5: VERY_LIKELY
            '''
            print("========== safe search ==========")
            safe_search = response.safe_search_annotation
            if 5 == safe_search.racy or 5 == safe_search.adult:
                return Response("Safe search", status=status.HTTP_400_BAD_REQUEST)

            '''
            # 2. recognize human eyes
            White list with index(a-z) is used to recognize human eyes
            Create parsing json module for the white list referenced by conf.custom_utils
            We use lower case always, so upper case converts to lower case
            '''
            print("========== label annotations ==========")
            if recognize_human_eye(response.label_annotations) is False:
                return Response("Bad image", status=status.HTTP_400_BAD_REQUEST)

            '''
            # 3. What state is the eyes
            '''
            print("========== web detections ==========")
            diagnosis = analysis_eyes(response.web_detection)

            print("[DEB] to be saved data", collect_diagnosis(request.data["user_id"],
                                                              response.label_annotations,
                                                              response.web_detection.best_guess_labels,
                                                              response.web_detection.web_entities,
                                                              diagnosis))

            # save results into database
            # web_detections = response.web_detection
            print("========= save ==========")
            '''
            collection = collect_diagnosis(request.data["user_id"],
                                           response.label_annotations,
                                           response.web_detection.best_guess_labels,
                                           response.web_detection.web_entities,
                                           diagnosis)
            diagnosis_serializer = DiagnosisSerializer(data=collection)

            #diagnosis_serializer.save()
            '''
            file_serializer.save()
            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            return Response("Invalid file", status=status.HTTP_400_BAD_REQUEST)


class DiagnosisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.AllowAny, ]


class EyeImageList(generics.ListAPIView):
    queryset = EyeImage.objects.all()
    serializer_class = EyeImageSerializer
    permission_classes = [permissions.AllowAny, ]


'''
Internal functions
'''


def get_permissions(self):
    if self.action == 'list':
        permission_classes = [AllowAny, ]
    else:
        permission_classes = [AllowAny, ]
    return [permission() for permission in permission_classes]


def get_google_vision_response(photo):
    print("[DEB] get google vision response")
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    content = photo['eye_photo'].read()

    response = client.annotate_image({
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
    })

    return response


def recognize_human_eye(labels):
    label_score = 0

    for l in labels:
        print("[DEB] desc:", l.description)
        print("[DEB] score:", l.score)
        if 0.9 > l.score:
            break

        first_char = l.description[0]
        whitelist_by_index = get_whitelist_value(first_char.lower())
        refusal_list_by_index = get_refusal_value(first_char.lower())

        if l.description.lower() in whitelist_by_index:
            print(l.description.lower())
            print(whitelist_by_index)
            label_score += 1

        if any(l.description.lower() is s for s in refusal_list_by_index):
            print(l.description.lower())
            print(refusal_list_by_index)
            return False

    if get_whitelist_score_value() > label_score:
        print("[DEB] not enough score: %d" % label_score)
        return False

    print("[DEB] score value: ", label_score)

    return True


def analysis_eyes(web_detections):
    best_guess = web_detections.best_guess_labels
    web_entities = web_detections.web_entities
    print("[DEB] best guess: ", best_guess)
    print("[DEB] web entities: ", web_entities)

    # best guess
    for b in best_guess:
        first_char = b.label[0]
        disease_list_by_index = get_disease_value(first_char.lower())
        if b.label.lower() in disease_list_by_index:
            print("Success: Disease[%s]" % b.label.lower())
            # return Response("Success: Disease[%s]" % b.label.lower(), status=status.HTTP_201_CREATED)

    # web entities
    for w in web_entities:
        print("[DEB] desc: ", w.description)
        print("[DEB] score: ", w.score)
        first_char = w.description[0]
        disease_list_by_index = get_disease_value(first_char.lower())

        if w.description.lower() in disease_list_by_index:
            print("Success: Disease[%s]" % w.description.lower())
            # return Response("Success disease: %s" % w.description.lower(), status=status.HTTP_201_CREATED)

    print("[DEB] end of the image analysis")

    diagnosis = "conjunctivitis"
    return diagnosis


def collect_diagnosis(user_id, labels, best_guess, web_entities, diagnosis):
    return {
        "user_id": user_id,
        "label": labels,
        "best_guess": best_guess,
        "web_entities": web_entities,
        "diagnosis": diagnosis
    }
