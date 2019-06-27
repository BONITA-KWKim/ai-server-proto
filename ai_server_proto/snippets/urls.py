from django.urls import path
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from . import views

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('', views.api_root),
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('schema/', schema_view),
    path(r'snippets/flavor/', views.FlavorList.as_view()),
    path(r'snippets/flavor/<int:pk>/', views.FlavorDetail.as_view()),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
