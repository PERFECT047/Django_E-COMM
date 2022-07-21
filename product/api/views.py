from rest_framework import status
from rest_framework.response import Response
from product.models import Product
from product.models import Category
from .serializers import ProductSerializers, CategorySerializers

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from product.api import serializers


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

@api_view(['GET',])
def product_detail_view(request, pk):
    try:
        products = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ProductSerializers(products)
        return Response(serializer.data)

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers