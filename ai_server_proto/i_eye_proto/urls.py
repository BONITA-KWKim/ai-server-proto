from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'checklist', views.CheckListViewSet, base_name='checklist')

urlpatterns = [
    path('', views.index, name='index'),
    path('version/', views.version_info, name='version'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    #path('checklist/', views.CheckList.as_view(), name='checklist'),
    #path('checklist/<int:pk>', views.CheckListDetail.as_view(), name='checklist_detail'),
    path('', include(router.urls)),
]
