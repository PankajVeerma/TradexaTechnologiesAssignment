
from rest_framework.generics import ListAPIView

from .models import Box
from .serializers import BoxSerializer


class BoxListAPIView(ListAPIView):
    queryset = Box.objects.all().order_by("cost", "id")
    serializer_class = BoxSerializer
