from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'version/', views.version_info, name='version'),
    path(r'users/', views.UserList.as_view(), name='user_list'),
    path(r'users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path(r'diagnoses/', views.DiagnosisList.as_view(), name='diagnosis_list'),
    path(r'diagnoses/<int:pk>', views.DiagnosisDetail.as_view(), name='diagnosis_detail'),
    path(r'eyePhotos/', views.EyeImageList.as_view(), name='eye_photos_list'),
]
