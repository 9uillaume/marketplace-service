from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validated_data):
        print("####")
        print(validated_data)  # Add this line for debugging
        return super().create(validated_data)  # Call the parent create()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
