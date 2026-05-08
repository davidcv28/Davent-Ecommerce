from ..models import Brand, Products, Category, Comments, valoration
from rest_framework import serializers
from django.db import transaction
from django.db.models import aggregates, Count, Sum
import re

#########################################################################
###### GESTIÓN DE PRODUCTOS
###### Serializador completo para CRUD de productos con validaciones de negocio
#########################################################################

class RegisterProductSerializer(serializers.ModelSerializer):
    name_product = serializers.CharField(
        label = 'Nombre del producto',
        style = {'placeholder':'Escribe el nombre del producto'},
        required = True,
        
        trim_whitespace = True
    )
    Producto = serializers.ReadOnlyField(source = 'name_product')
    price_product = serializers.DecimalField(
        label = 'Precio del producto',
        style = {'placeholder':'Escribe el precio del producto'},
        required = True,
        
        max_digits=12,
        decimal_places=2
    )
    Precio = serializers.ReadOnlyField(source = 'price_product')
    stock_product = serializers.IntegerField(
        label = 'Stock de producto',
        style = {'placeholder':'Escribe el stock actual del producto'},
        required = True,
        
        
    )
    Stock = serializers.ReadOnlyField(source = 'stock_product')
    category_product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar categoria',
        queryset = Category.objects.all(),
        
        allow_null = False
    )
    Categoria = serializers.ReadOnlyField(source = 'category_product.name_category')
    brand_product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar marca',
        queryset = Brand.objects.all(),
        allow_null = False,
    
    )
    Marca = serializers.ReadOnlyField(source='brand_product.name_brand')
    img_product = serializers.ImageField(
        label = 'Subir imagen del producto',
        style = {'help_text':'Solo se admiten imagenes en formato png', 'accept':'image/png', 'required':'required'},
    
    )
    Imagen = serializers.ReadOnlyField(source='img_product.url')
    class Meta:
        model = Products
        fields = ['name_product','Producto','price_product','Precio','stock_product','Stock','category_product','Categoria','brand_product','Marca','img_product','Imagen']
    def validate_name_product(self, value):
        product_obj = value.upper().strip()
        queryset = Products.objects.filter(name_product__iexact = product_obj)
        letter_count = 0
        errors = []
        if len(product_obj) < 3:
            errors.append('El nombre del producto debe tener al menos 3 caracteres')
        for letter in product_obj:
            if letter.isalpha():
                letter_count+=1
        if letter_count < 2:
            errors.append('El nombre del producto debe tener al menos 2 letras')
        if re.search(r'[^a-zA-Z0-9ñÑ\s\-\.]', product_obj):
            errors.append('El nombre ingresado posee un caracter especial no admitido')
        if self.instance:
            queryset = queryset.exclude(pk = self.instance.pk)
        if queryset.exists():
            errors.append('El nombre del producto ingresado ya existe')
        if errors:
            raise serializers.ValidationError(errors)
        return product_obj
    def validate_price_product(self, value):
        price_obj = value
        errors = []
        if not price_obj:
            errors.append('Porfavor ingrese un precio')
        if price_obj < 1:
            errors.append('El precio minimo debe ser $1')
        if price_obj > 99999999:
            errors.append('Limite maximo de precio superado')
        if errors:
            raise serializers.ValidationError(errors)
        return price_obj
    def validate_stock_product(self, value):
        stock_obj = value
        errors = []
        if not stock_obj:
            errors.append('Porfavor ingrese un stock para el producto')
        if stock_obj <0:
            errors.append('El stock minimo permitido es 0')
        if stock_obj > 9999:
            errors.append('Stock maximo superado')
        if errors:
            raise serializers.ValidationError(errors)
        return stock_obj
    def validate_img_product(self, value):
        img_obj = value
        allow_content = ['image/png']
        errors = []
        if img_obj:
            if img_obj.content_type not in allow_content:
                errors.append('Formato de imagen no valido, solo se acepta .png') 
            if img_obj.size > 5*1024*1024:
                errors.append('El tamaño de la imagen es demasiado grande')
            if errors:
                raise serializers.ValidationError(errors)
        return img_obj


#########################################################################
###### GESTIÓN DE CATEGORÍAS
###### Asegura que las categorías mantengan un estándar de nombrado
#########################################################################
class RegisterCategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name_category = serializers.CharField(
        label = 'Nombre de categoria',
        style = {'placeholder':'Escribe el nombre de la categoria'},
        required = True,
        trim_whitespace = True
    )
    Categoria = serializers.ReadOnlyField(source = 'name_category')
    class Meta:
        model = Category
        fields = ['id', 'name_category', 'Categoria']
    def validate_name_category(self, value):
        category_obj = value.upper().strip()
        queryset = Category.objects.filter(name_category__iexact = category_obj)
        letter_count = 0
        errors = []
        if len(category_obj) < 3:
            errors.append('El nombre de la categoria debe tener al menos 3 caracteres')
        for letter in category_obj:
            if letter.isalpha():
                letter_count += 1
        if letter_count < 3:
            errors.append('El nombre de la categoria debe tener al menos 3 letras')
        if re.search(r'[^a-zA-Z\s]', category_obj):
            errors.append('El nombre no puede llevar numeros ni caracteres especiales')
        if self.instance:
            queryset = queryset.exclude(pk = self.instance.pk)
        if queryset.exists():
            errors.append('El nombre de la categoria ingresada ya existe')
        if errors:
            raise serializers.ValidationError(errors)
        return category_obj

        

#########################################################################
###### GESTIÓN DE MARCAS
###### Valida unicidad y previene caracteres especiales no deseados
#########################################################################
class RegisterBrandSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name_brand = serializers.CharField(
        label = 'Nombre de marca',
        style = {'placeholder':'Escribe el nombre de la marca'},
        trim_whitespace = True
    )
    Marca = serializers.ReadOnlyField(source = 'name_brand')
    class Meta:
        model = Brand
        fields = ['id','name_brand','Marca']
    def validate_name_brand(self, value):
        brand_obj = value.upper().strip()
        queryset = Brand.objects.filter(name_brand__iexact = brand_obj)
        errors = []
        if len(brand_obj) < 3:
            errors.append('El nombre de la marca debe tener al menos 3 caracteres')
        if re.search(r'[^a-zA-Z0-9ñÑ\s\.\-]', brand_obj):
            errors.append('El nombre de la marca pose un caracter especial no permitido')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            errors.append('El nombre de la marca ingresada ya existe')
        if errors:
            raise serializers.ValidationError(errors)
        return brand_obj


#########################################################################
###### SISTEMA DE VALORACIONES (REVIEWS)
###### Calcula automáticamente el promedio de valoración del producto al crear
#########################################################################

class RegisterValorationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )
    Usuario = serializers.ReadOnlyField(
        source = 'user.username'
    )
    product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar producto',
        queryset = Products.objects.all(),
        write_only = True,
        allow_null = False
    )
    Producto = serializers.ReadOnlyField(
        source = 'product.name_product'
    )
    rating = serializers.IntegerField(
        label = 'Valoración',
        style = {'placeholder':'Valorar'},
        write_only = True,
        default = 1
    )
    Valoración = serializers.ReadOnlyField(source = 'rating')
    class Meta:
        model = valoration
        fields = ['id', 'user','Usuario','product','Producto','rating','Valoración']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset = valoration.objects.all(),
                fields = ['user', 'product'],
                message= 'No puedes valorar el mismo producto 2 veces'
            )
        ]
    def validate_rating(self, value):
        rating_obj = value
        errors = []
        if  not rating_obj or rating_obj <1 or rating_obj >5:
            errors.append('Porfavor ingrese una valoración valida')
        if errors:
            raise serializers.ValidationError(errors)
        return rating_obj
    
    @transaction.atomic
    def create(self, validated_data):
        valoration_instance = super().create(validated_data)
        select_product = validated_data.get('product')
        valortion_product = valoration.objects.filter(product = select_product).aggregate(
            total_count = Count('id'),
            total_sum = Sum('rating')
        )
        total_count_valoration = valortion_product.get('total_count')
        total_sum_valoration = valortion_product.get('total_sum')
        if total_count_valoration == 0:
            total_avg_valoration = 0
        else:
            total_avg_valoration = total_sum_valoration / total_count_valoration
        select_product.valoration = round(total_avg_valoration, 2)
        select_product.save()
        return valoration_instance

#########################################################################
###### SISTEMA DE COMENTARIOS
###### Permite a los usuarios dejar feedback textual en los productos
#########################################################################
class RegisterCommentSerializer ( serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    Comentario= serializers.CharField(
        label = 'Comentario',
        style = {'placeholder':'Escribe tu comentario','base_template':'textarea.html','rows':3},
        required = True,
        trim_whitespace = False,
        source = 'comment'
    )
    Fecha=serializers.ReadOnlyField(source='datetime')
    username = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )
    Usuario = serializers.ReadOnlyField(
        source='user.username'
    )
    Producto = serializers.PrimaryKeyRelatedField(
        source = 'product',
        queryset = Products.objects.all(),
        allow_null = False
    )
    class Meta:
        model = Comments
        fields = ['id','Comentario','username','Usuario','Producto','Fecha']
    def validate_Comentario(self, value):
        comment_obj = value.strip()
        errors = []
        if len(comment_obj)< 6:
            errors.append('El comentario debe tener al menos 6 caracteres')
        if errors:
            raise serializers.ValidationError(errors)
        return comment_obj
