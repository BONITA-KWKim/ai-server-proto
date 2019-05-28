from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('version/', views.version_info, name='version'),
    path('checklist/', views.CheckList.as_view(), name='checklist'),
    path('checklist/<int:pk>', views.CheckListDetail.as_view(), name='checklist_detail'),
]