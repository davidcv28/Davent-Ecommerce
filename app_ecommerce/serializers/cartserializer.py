from rest_framework import serializers
from ..models import Cart, CartItem, Products
from django.conf import Settings

#####REGISTER ITEM SERIALIZER
class RegisterItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar producto',
        queryset = Products.objects.all(),
        write_only = True
    )
    Producto = serializers.SlugRelatedField(
        source = 'product',
        slug_field = 'name_product',
        read_only = True
    )
    Precio = serializers.SlugRelatedField(
        source = 'product',
        slug_field = 'price_product',
        read_only = True
    )
    Cantidad = serializers.IntegerField(
        label = 'Ingrese cantidad',
        style = {'placeholder':'Ingresar cantidad'},
        default = 1,
        source = 'quantity'
    )
    SubTotal = serializers.ReadOnlyField(source = 'subtotal')
    class Meta:
        model = CartItem
        fields = ['product', 'Producto','Precio','Cantidad','SubTotal']
    def validate_Cantidad(self, value):
        quantity_obj = value
        if quantity_obj is None or quantity_obj <1:
            quantity_obj = 1
        if quantity_obj >99:
            quantity_obj = 99
        return quantity_obj
    def create(self, validated_data):
        user = self.context.get('request').user
        cart_user = Cart.objects.get(user=user)
        product = validated_data.get('product')
        item_instance = CartItem.objects.filter(cart = cart_user, product = product).first()
        if item_instance:
            item_instance.quantity = validated_data.get('quantity')
            item_instance.save()
            return item_instance
        validated_data['cart']=cart_user
        return super().create(validated_data)

####LIST CART SERIALIZER
class ListCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault)
    Usuario = serializers.SlugRelatedField(source = 'user', slug_field = 'username', read_only = True)
    Carrito = RegisterItemSerializer(read_only = True, many = True, source='items')
    PrecioTotal = serializers.ReadOnlyField(source = 'total_price')
    Fecha=serializers.ReadOnlyField(source='created_at')
    class Meta:
        model = Cart
        fields = ['user','Usuario', 'Carrito','PrecioTotal','Fecha']

    