from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Box, Order, Product
from .serializers import BoxSerializer, OrderSerializer, ProductSerializer
from .services import recommend_box_for_order


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer

    @action(detail=True, methods=["get"], url_path="recommend-box")
    def recommend_box(self, request, pk=None):
        order = self.get_object()

        try:
            result = recommend_box_for_order(order)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if result.fits_single_box:
            return Response(
                {
                    "order_number": order.order_number,
                    "fits_single_box": True,
                    "recommended_box": BoxSerializer(result.box).data,
                }
            )

        return Response(
            {
                "order_number": order.order_number,
                "fits_single_box": False,
                "reason": result.reason,
                "boxes": [
                    {
                        "box": BoxSerializer(b.box).data,
                        "items": [u.sku for u in b.units],
                        "used_weight_kg": round(b.used_weight, 3),
                        "used_volume_cm3": round(b.used_volume, 2),
                    }
                    for b in (result.bins or [])
                ],
            }
        )
