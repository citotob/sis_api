
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'', views.ListVendorPerformance, basename='get')
# urlpatterns = router.urls

getByVendor = views.VendorPerformanceAPI.as_view({
    'get': 'getByVendor',
})
getAll = views.VendorPerformanceAPI.as_view({
    'get': 'getAll',
})
create = views.VendorPerformanceAPI.as_view({
    'post': 'create'
})
update = views.VendorPerformanceAPI.as_view({
    'post': 'update'
})

urlpatterns = [
    path('all/', getAll),
    path('vendor/', getByVendor),
    path('create/', create),
    path('update/', update),
]

urlpatterns = format_suffix_patterns(urlpatterns)
