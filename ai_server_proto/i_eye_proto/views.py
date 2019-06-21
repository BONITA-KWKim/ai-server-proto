import logging

from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Diagnosis
from .models import EyeImage
from .serializers import UserSerializer
from .serializers import DiagnosisSerializer
from .serializers import EyeImageSerializer
from .custom_utils.i_eye_permissions import get_permissions
from .image_analyses.i_eye_google_vision import get_google_vision_response
from .image_analyses.i_eye_image_analyses import recognize_human_eye
from .image_analyses.i_eye_image_analyses import analysis_eyes
from .image_analyses.i_eye_utils import collect_diagnosis

# Create your views here.
logger = logging.getLogger('ai_server_proto.i_eye_proto')


@api_view(['GET'])
def index(request):
    return HttpResponse("I-EYE Prototype AI server")


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


"""
diagnosis
"""


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
                return Response("Safe search",
                                status=status.HTTP_400_BAD_REQUEST)

            '''
            # 2. recognize human eyes
            White list with index(a-z) is used to recognize human eyes.
            Create parsing json module for the white list referenced by 
            conf.custom_utils.
            We use lower case always, so upper case converts to lower case.
            '''
            print("========== label annotations ==========")
            if recognize_human_eye(response.label_annotations) is False:
                return Response("Bad image",
                                status=status.HTTP_400_BAD_REQUEST)

            '''
            # 3. What state is the eyes
            '''
            print("========== web detections ==========")
            diagnosis = analysis_eyes(response.web_detection)

            print("[DEB] to be saved data",
                  collect_diagnosis(request.data["user_id"],
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
