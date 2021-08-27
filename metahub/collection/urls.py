from django.urls import path

from metahub.collection import views

urlpatterns = [
    path(
        "synchronise/",
        views.synchronise,
        name="synchronise",
    ),
]
