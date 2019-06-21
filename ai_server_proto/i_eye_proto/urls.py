from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(
        regex=r"^$",
        view=views.index,
        name="index"
    ),
    # path(r'', views.index, name='index'),
    url(r'^version/$', views.version_info, name='version'),
    url(r'^users/$', views.UserList.as_view(), name='user_list'),
    url(r'^users/<int:pk>/$', views.UserDetail.as_view(), name='user_detail'),
    url(r'^diagnoses/$', views.DiagnosisList.as_view(), name='diagnosis_list'),
    url(
        regex=r'^diagnoses/<int:pk>$',
        view=views.DiagnosisDetail.as_view(),
        name='diagnosis_detail'
    ),
    path(r'eyePhotos/', views.EyeImageList.as_view(), name='eye_photos_list'),
]
