from rest_framework import serializers
from .models import Product, Category, ProductList
from accounts.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['thumbnail']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        category = CategorySerializer(data=Category.objects.filter(pk=data['category']), many=True)
        category.is_valid()
        data['category'] = category.data
        return data


class CommonProductSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        product = ProductSerializer(data=Product.objects.filter(id=obj['product']), many=True,
                                    context={'request': self.context['request']})
        product.is_valid()
        return product.data


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = ['quantity', 'product']


class OrderCreateSerializer(serializers.Serializer):
    """
    I changed client data to username here, beacuse neither name or surname is unique, so i can't identify user based
    on that. Other option was to use currently authenticated user.
    """
    username = serializers.CharField()
    delivery_address = serializers.CharField()
    product_list = ProductListSerializer(many=True)

    def validate_username(self, value):
        if not CustomUser.objects.filter(username=value).exists():
            serializers.ValidationError("User does not exists")
        return value
