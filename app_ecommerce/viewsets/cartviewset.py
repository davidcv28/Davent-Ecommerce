from rest_framework import viewsets, response, permissions, mixins, status
from rest_framework.response import Response
from ..permissions import IsStaffUser
from ..serializers import cartserializer
from ..models import Cart, CartItem
from django.conf import Settings

####CART LIST VIEWSET
class CartListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = cartserializer.ListCartSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Cart.objects.select_related('user').filter(user = self.request.user)


####CART ITEM REGISTER VIEWSET
class CartItemRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = cartserializer.RegisterItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.select_related('cart','product').all()
    