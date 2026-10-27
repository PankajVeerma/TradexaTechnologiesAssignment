
from rest_framework.generics import ListAPIView

from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
