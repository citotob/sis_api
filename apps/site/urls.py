from django.urls import path
from survey import views
from rest_framework.authtoken import views as tokenview


urlpatterns = [
    # path('login/', tokenview.obtain_auth_token),
    path('addbatch/', views.addbatch),
]
