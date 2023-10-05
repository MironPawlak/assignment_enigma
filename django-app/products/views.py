import datetime
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db.models import Sum
from .models import Product, Order, ProductList
from .serializers import ProductSerializer, OrderCreateSerializer, CommonProductSerializer
from accounts.permissions import IsSellerOrReadOnly, IsCustomer, IsSeller
from accounts.models import CustomUser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsSellerOrReadOnly]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'description', 'price']
    ordering_fields = ['name', 'category', 'price']


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        v_data = serializer.validated_data
        sum_price = 0
        for prod in v_data['product_list']:
            sum_price += prod['quantity'] * prod['product'].price
        user = CustomUser.objects.filter(username=v_data['username']).first()
        due_date = datetime.datetime.today() + datetime.timedelta(days=5)
        data = {
            'client': user,
            'delivery_address': v_data['delivery_address'],
            'order_date': datetime.datetime.today(),
            'due_date': due_date,
            'sum_price': sum_price
        }
        order = Order(**data)
        order.save()
        for d in v_data['product_list']:
            product = ProductList.objects.create(order=order, **d)
            product.save()
        return Response(data={'Total price': sum_price, 'Due date': due_date}, status=status.HTTP_201_CREATED)


class CommonProductsFilter(filters.FilterSet):
    start_date = filters.DateFilter(label='start_date')
    end_date = filters.DateFilter(label='end_date')
    limit = filters.NumberFilter(label='limit')


class CommonProductsListView(generics.ListAPIView):
    serializer_class = CommonProductSerializer
    filterset_class = CommonProductsFilter
    permission_classes = [IsAuthenticated, IsSeller]
    queryset = ProductList.objects.all()

    def filter_queryset(self, q):
        if start := self.request.query_params.get('start_date'):
            q = q.filter(order__order_date__gte=start)
        if end := self.request.query_params.get('end_date'):
            q = q.filter(order__order_date__lte=end)
        q = q.values('product').annotate(total=Sum('quantity')).order_by('-total')
        if limit := self.request.query_params.get('limit'):
            q = q[:int(limit)]
        return q
