
from django.urls import path

from .views import BoxListAPIView

urlpatterns = [
    path("box-list/", BoxListAPIView.as_view(), name="box-list"),
]
