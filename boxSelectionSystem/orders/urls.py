
from django.urls import path

from .views import RecommendBoxAPIView

urlpatterns = [
    path(
        "<int:order_id>/recommend-box/",
        RecommendBoxAPIView.as_view(),
        name="recommend-box",
    ),
]
