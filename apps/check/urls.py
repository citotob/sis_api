from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

load = views.checkAPI.as_view({
    'post': 'load',
})
network = views.checkAPI.as_view({
    'post': 'network',
})
database = views.checkAPI.as_view({
    'post': 'database',
})
bruteforce = views.checkAPI.as_view({
    'post': 'bruteforce',
})
disk = views.checkAPI.as_view({
    'POST': 'disk',
})

urlpatterns = [
    path('load/', load),
    path('network/', network),
    path('database/', database),
    path('bruteforce/', bruteforce),
    path('disk/', disk),
]

urlpatterns = format_suffix_patterns(urlpatterns)
