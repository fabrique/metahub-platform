from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'get_object_by_inventory_number', views.get_object_by_inventory_number),
    url(r'get_story_by_id', views.get_story_by_id),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]