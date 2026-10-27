
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from boxes.serializers import BoxSerializer
from .models import Order, BoxRecommendation
from .services import recommend_box, NoSuitableBoxError


class RecommendBoxAPIView(APIView):

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        try:
            box = recommend_box(order)
        except NoSuitableBoxError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        recommendation, created = (
            BoxRecommendation.objects.update_or_create(
                order=order,
                defaults={"box": box},
            )
        )

        return Response(
            {
                "order_id": order.id,
                "recommended_box": BoxSerializer(box).data,
                "recommendation_saved": True,
            },
            status=status.HTTP_200_OK,
        )
