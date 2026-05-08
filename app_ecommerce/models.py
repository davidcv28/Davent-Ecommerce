from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Aggregate, Sum, F
from cloudinary.models import CloudinaryField

#### PERFIL MODEL #####
class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    image = CloudinaryField('image', folder='perfil', default = "perfil/usuario.png")
    balance = models.DecimalField( max_digits=12, decimal_places=2, default=300000)

########################
### PRODUCTS MODELS ####
########################

class Category(models.Model):
    name_category = models.CharField( max_length=150, unique=True)

    def __str__(self):
        return f"{self.name_category}"
    

class Brand(models.Model):
    name_brand = models.CharField(max_length=150, unique= True)

    def __str__(self):
        return f"{self.name_brand}"
class Products(models.Model):
    name_product = models.CharField( max_length=150, unique=True, null=False)
    stock_product = models.IntegerField(default = 0)
    price_product = models.DecimalField( max_digits=14, decimal_places=2, default = 0.00)
    category_product = models.ForeignKey('Category', on_delete=models.SET_NULL, null = True)
    brand_product = models.ForeignKey('Brand', on_delete=models.SET_NULL, null = True)
    img_product = CloudinaryField('image', folder='productos', blank=True, null=True)
    valoration_product = models.IntegerField(default=0, null=True)
    
    def __str__(self):
        return f"{self.name_product},    ${self.price_product},     Stock: {self.stock_product}"

    def stock_enable(self):
        

        return self.stock_product > 1

class Comments(models.Model):
    comment = models.CharField(max_length=2500, null = False, blank = False)
    datetime = models.DateField(  default=timezone.now )
    product = models.ForeignKey("Products",  on_delete=models.CASCADE, null=True, related_name='comment_product')
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class valoration (models.Model):
    rating = models.IntegerField(default=0)
    product = models.ForeignKey("Products", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'product'],
                name = 'unique_valoration_constraint',
                violation_error_message='No puedes valorar un mismo producto 2 veces',
            )
        ]
##################################
#############CART MODEL###########
##################################
class Cart (models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    created_at = models.DateField(default = timezone.now)
    def __str__(self):
        return f'Carrito de {self.user.username}'
    @property
    def total_price(self):
        return self.items.aggregate(total = Sum(F('quantity') * F('product__price_product')))['total'] or 0
    @property
    def total_quantity(self):
        return self.items.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['product', 'cart'],
                name = 'unique_cart_item'
            )
        ]
    def quantity_max(self):
        if self.quantity > 99:
            self.quantity = 99
        return self.quantity
    @property
    def subtotal(self):
        return self.quantity * self.product.price_product
class Pucharse_order(models.Model):
    order_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField( default=timezone.now)
    order_total = models.DecimalField( max_digits=12, decimal_places=2, default=0)
    order_total_price = models.DecimalField(max_digits = 12, decimal_places = 2, default= 0)
    iva = models.DecimalField( max_digits=10, decimal_places=2, null=True ,default =21)
    n_invoice = models.CharField(max_length=50, null = True, unique= True, blank=True)
    class Meta:
        
        db_table = 'app_ecommerce_pucharse_order' 
    
            

class Pucharse_order_detail(models.Model):
    detail_order = models.ForeignKey('Pucharse_order', on_delete=models.PROTECT, related_name="items")
    detail_product = models.ForeignKey("Products", on_delete=models.CASCADE)
    detail_quantity= models.IntegerField(default=1)
    detail_price = models.DecimalField( max_digits=12, decimal_places=2)
    detail_total = models.DecimalField(max_digits=12, decimal_places=2 ,default=0)


 