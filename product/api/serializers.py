from rest_framework import serializers
from rest_framework.fields import ModelField

from product.models import Category, Product

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'seller', 'title', 'slug', 'description', 'price', 'image', 'thumbnail', 'reviews')