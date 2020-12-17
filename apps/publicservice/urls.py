from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

clusterpenduduk = views.publicServiceAPI.as_view({
    'get': 'clusterpenduduk',
})

urlpatterns = [
    path('clusterpenduduk/', clusterpenduduk),
]

urlpatterns = format_suffix_patterns(urlpatterns)
