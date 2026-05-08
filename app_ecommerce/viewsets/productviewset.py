from rest_framework import viewsets, mixins, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import OrderingFilter
from ..serializers import productserializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Products, Category, Brand, Comments, valoration
from ..permissions import IsStaffUser
from django_filters.rest_framework import DjangoFilterBackend
from ..filterset import ProductFilterSet

####REGISTER PRODUCT VIEWSET
class RegisterProductViewSet(viewsets.ModelViewSet):
    serializer_class = productserializer.RegisterProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Products.objects.select_related('category_product', 'brand_product').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilterSet
    ordering_fields = ['price_product']
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission = [permissions.IsAuthenticated()]
        else:
            permission = [IsStaffUser()]
        return permission
    def get_object(self):
        return super().get_object()

####REGISTER CATEGORY VIEWSET
class RegisterCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = productserializer.RegisterCategorySerializer
    permission_classes = [IsStaffUser]
    queryset = Category.objects.all()
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data = request.data, instance = instance, context={'request':request}, partial = True)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        return Response(serializer.data)
####REGISTER BRAND VIEWSET
class RegisterBrandViewSet(viewsets.ModelViewSet):
    serializer_class = productserializer.RegisterBrandSerializer
    permission_classes = [IsStaffUser]
    queryset = Brand.objects.all()
    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(data = request.data, instance =instance , context = {'request':request},  partial = True)
            serializer.is_valid(raise_exception = True)
            self.perform_update(serializer)
            return Response(serializer.data)
####REGISTER VALORATION VIEWSET
class RegisterValorationViewSet(viewsets.GenericViewSet):
    serializer_class = productserializer.RegisterValorationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return valoration.objects.select_related('user','product').all()
        return valoration.objects.select_related('user','product').filter(user = self.request.user)

####REGISTER COMMENTS VIEWSET
class RegisterCommentsViewSet(viewsets.ModelViewSet):
    serializer_class = productserializer.RegisterCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comments.objects.all()