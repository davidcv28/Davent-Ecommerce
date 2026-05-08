from rest_framework import serializers, viewsets, mixins, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter
from app_ecommerce.models import Perfil, Cart, Category, Brand, Products, Comments, valoration
from django.conf import Settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re, django_filters
from django.db import transaction, models
from django.utils import timezone
from django.db.models import Sum, Count, Avg, F
from django import forms

#########################################################################
###### SERIALIZADORES DE USUARIOS (STAFF)
###### Maneja el registro de administradores con validaciones de seguridad
#########################################################################

class RegisterUserStaffSerializer(serializers.ModelSerializer):
    Nombre = serializers.CharField(
        source = 'first_name',
        label = 'Nombre',
        style = {'placeholder':'Escribe tu nombre'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    Apellido = serializers.CharField(
        source = 'last_name',
        label = 'Apellido',
        style = {'placeholder':'Escribe tu apellido'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    Usuario = serializers.CharField(
        source = 'username',
        label = 'Nombre de usuario',
        style = {'placeholder':'Escribe tu nombre de usuario'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    Correo = serializers.EmailField(
        source = 'email',
        label = 'Correo',
        style = {'placeholder':'Escribe tu correo'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    Contraseña = serializers.CharField(
        source = 'password',
        label = 'Contraseña',
        style = {'placeholder':'Escribe tu contraseña'},
        required = True,
        write_only = True
    )
    Contraseña2 = serializers.CharField(
        label = 'Confirmar contraseña',
        style = {'placeholder':'Repite tu contraseña'},
        required = True,
        write_only = True
    )
    Administrador = serializers.BooleanField(
        source = 'is_staff',
        label = 'Es un administrador?',
        required = True
    )
    class Meta:
        model = Settings.AUTH_USER_MODEL
        fields = ['Nombre','Apellido','Usuario','Correo','Contraseña','Contraseña2','Administrador']
    
    def validate_Nombre(self, value):
        name_obj = value.upper().strip()
        errors = []
        letter_count = 0
        if len(name_obj) < 4:
            errors.append('El nombre debe tener al menos 4 caracteres')
        if re.search(r'[^a-zA-Z\sñÑ]', name_obj):
            errors.append('El nombre solo puede llevar letras y espacios')
        for letter in name_obj:
            if letter.isalpha():
                letter_count+=1
        if letter_count < 4:
            errors.append('El nombre debe llevar al menos 4 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return name_obj
    
    def validate_Apellido(self, value):
        last_name_obj = value.upper().strip()
        errors = []
        letter_count = 0
        if len(last_name_obj) < 4:
            errors.append('El apellido debe tener al menos 4 letras')
        if re.search(r'[^a-zA-Z\sñÑ]', last_name_obj):
            errors.append('Solo se admiten letras y espacios')
        for letter in last_name_obj:
            if letter.isalpha():
                letter_count +=1

        if letter_count < 4:
            errors.append('El apellido debe llevar al menos 4 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return last_name_obj
    
    def validate_Usuario(self, value):
        username_obj = value.strip()
        errors = []
        queryset = User.objects.filter(username__iexact = username_obj)
        if len(username_obj)< 4:
            errors.append('El nombre de usuario al menos debe tener 4 caracteres')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            errors.append('El nombre de usuario ingresado ya esta en uso')
        if errors:
            raise serializers.ValidationError(errors)
        return username_obj
    
    def validate_Correo(self, value):
        email_obj = value.strip()
        queryset = User.objects.filter(email__iexact = email_obj)
        errors = []
        domain_exist = False
        allow_domains =['@hotmail.com', '@gmail.com','@yahoo.com','@outlook.com','@live.com']
        for domain in allow_domains:
            if email_obj.endswith(domain):
                domain_exist=True
        if not domain_exist:
            errors.append('Dominio ingresado no valido')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            errors.append('El correo ingresado ya esta en uso')
        if errors:
            raise serializers.ValidationError(errors)
        return email_obj
    
    def validate_Contraseña(self, value):
        password_obj = value
        errors = []
        if len(password_obj) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres')
        if  not re.search(r'[a-zñ]', password_obj):
            errors.append('La contraseña debe tener al menos una letra minuscula')
        if not re.search(r'[A-ZÑ]', password_obj):
            errors.append('La contraseña debe tener al menos una letra mayuscula')
        if not re.search(r'[0-9]', password_obj):
            errors.append('La contraseña debe tener al menos un numero')
        if not re.search(r'[^a-zA-Z0-9ñÑ]', password_obj):
            errors.append('La contraseña debe tener al menos un caracter especial')
        if errors:
            raise serializers.ValidationError(errors)
        return password_obj
    
    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('Contraseña2')
        errors = {}
        if password1 != password2:
            errors['Contraseña2'] = 'Las contraseñas no coinciden'
        
        attrs.pop('Contraseña2')
        return attrs
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            is_staff = validated_data.get('is_staff', False)
        )
        Cart.objects.create(user = user)
        return user




####REGISTER USER SERIALIZER
class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        label = 'Nombre',
        style = {'placeholder':'Escribe tu nombre'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    last_name = serializers.CharField(
        label = 'Apellido',
        style = {'placeholder':'Escribe tu apellido'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    username = serializers.CharField(
        label = 'Nombre de usuario',
        style = {'placeholder':'Escribe tu nombre de usaurio'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    email = serializers.EmailField(
        label = 'Correo electronico',
        style = {'placeholder':'Escribe tu correo'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    password = serializers.CharField(
        label = 'Contraseña',
        style = {'placeholder':'Escribe tu contraseña', 'input_type':'password'},
        required = True,
        write_only = True
    )
    password2 = serializers.CharField(
        label = 'Confirmar contraseña',
        style = {'placeholder':'Escribe tu contraseña', 'input_type':'password'},
        required = True,
        write_only = True
    )
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email','password','password2']
    
    def validate_first_name(self, value):
        name_obj = value.upper().strip()
        letter_count = 0
        errors = []
        if len(name_obj) < 4:
            errors.append('El nombre debe tener al menos 4 caracteres')
        if re.search(r'[^a-zA-Z\sñÑ]', name_obj):
            errors.append('Solo se adminten letras y espacios')
        for letter in name_obj:
            if letter.isalpha():
                letter_count+=1
        if letter_count < 4:
            errors.append('El nombre debe tener al menos 4 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return name_obj
    
    def validate_last_name(self, value):
        last_name_obj = value.upper().strip()
        errors = []
        letter_count = 0
        if len(last_name_obj) < 4:
            errors.append('El apellido debe tener al menos 4 caracteres')
        if re.search(r'[^a-zA-Z\sñÑ]', last_name_obj):
            errors.append('Solo se admiten letras y espacios')
        for letter in last_name_obj:
            if letter.isalpha():
                letter_count +=1
        if letter_count < 4:
            errors.append('El apellido debe tener al menos 4 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return last_name_obj
    def validate_username(self, value):
        user_obj = value.strip()
        queryset = User.objects.filter(username__iexact = user_obj)
        errors = []
        if len(user_obj) < 4:
            errors.append('El nombre de usuario debe tener al menos 4 caracteres')
        if queryset.exists():
            errors.append('El nombre de usuario ingresado ya esta en uso')
        if errors:
            raise serializers.ValidationError(errors)
        return user_obj

    def validate_email(self,value):
        email_obj = value.strip()
        allow_domains = ['@hotmail.com','@gmail.com','@outlook.com','@yahoo.com']
        domain_exist = False
        queryset = User.objects.filter(email__iexact = email_obj)
        errors = []
        for domain in allow_domains:
            if email_obj.endswith(domain):
                domain_exist=True
                break
        if not domain_exist:
            errors.append('Dominio ingresado no valido')
        if queryset.exists():
            errors.append('El correo ingresado ya se encuentra en uso')
        if errors:
            raise serializers.ValidationError(errors)
        return email_obj
    
    def validate_password(self, value):
        password_obj = value
        errors = []
        if len(password_obj)< 8:
            errors.append('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[a-zñ]', password_obj):
            errors.append('La contraseña debe tener al menos una letra minuscula')
        if not re.search(r'[A-ZÑ]', password_obj):
            errors.append('La contraseña debe tener al menos una letra mayuscula')
        if not re.search(r'[0-9]', password_obj):
            errors.append('La contraseña debe tener al menos un numero')
        if not re.search(r'[^a-zA-Z0-9ñÑ]', password_obj):
            errors.append('La contraseña debe tener al menos un caracter especial')
        if errors:
            raise    serializers.ValidationError(errors)
        return password_obj
    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password2')
        errors = {}
        if password1 != password2:
            errors['password2']='Las contraseñas no coinciden'
        if errors:
            raise serializers.ValidationError(errors)
        attrs.pop('password2')
        return attrs
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            email = validated_data['email'],
            password= validated_data['password']
        )
        Cart.objects.create(user = user)
        return user

#########################################################################
###### PERMISOS PERSONALIZADOS
#########################################################################

# Restringe acceso solo a usuarios no autenticados (Anónimos)
class Anonimouspermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        return False

# Restringe acceso solo a miembros del staff/administradores
class StaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

#########################################################################
###### VIEWSETS DE REGISTRO
###### Selecciona dinámicamente el serializador según el tipo de usuario
#########################################################################
class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return RegisterUserStaffSerializer
        return RegisterUserSerializer
    def get_permissions(self):
        if self.request.user.is_authenticated:
            return [StaffPermission()]
        return [Anonimouspermission()]
    queryset = User.objects.all()

#########################################################################
###### ACTUALIZACIÓN DE PERFIL Y SEGURIDAD
###### Serializadores para cambio de datos, contraseñas y multimedia
#########################################################################
class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        label = 'Nombre',
        style = {'placeholder':'Escribe tu nombre'},
        required = True,
        trim_whitespace = True
    )
    last_name = serializers.CharField(
        label = 'Apellido',
        style = {'placeholder':'Escribe tu apellido'},
        required = True,
        trim_whitespace = True
    )
    email = serializers.EmailField(
        label = 'Correo',
        style = {'placeholder':'Escribe tu correo'},
        required = True,
        trim_whitespace = True
    )
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
    
    def validate_first_name(self, value):
        name_obj = value.upper().strip()
        letter_count = 0
        errors = []
        if len(name_obj) < 4:
            errors.append('El nombre debe tener al menos 4 caracteres')
        if re.search (r'[^a-zA-Z\sñÑ]', name_obj):
            errors.append('Solo se admiten letras y espacios para el nombre')
        for letter in name_obj:
            if letter.isalpha():
                letter_count +=1
        if letter_count < 4:
            errors.append('El nombre debe tener al menos 4 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return name_obj
    def validate_last_name(self, value):
        last_name_obj = value.upper().strip()
        letter_count = 0
        errors = []
        if len(last_name_obj) < 4:
            errors.append('El apellido debe tener al menos 4 caracteres')
        if re.search (r'[^a-zA-Z\sñÑ]', last_name_obj):
            errors.append('Solo se admiten letras y espacios para el apellido')
        for letter in last_name_obj:
            if letter.isalpha():
                letter_count +=1
        if letter_count < 4:
            errors.append('El apellido debe tener al menos 4 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return last_name_obj
    def validate_email(self, value):
        email_obj = value.strip()
        queryset = User.objects.filter(email__iexact = email_obj)
        allow_domains = ['@gmail.com', '@hotmail.com','@yahoo.com','@outlook.com']
        domain_exists = False
        errors = []
        for domain in allow_domains:
            if email_obj.endswith(domain):
                domain_exists = True
                break
        if not domain_exists:
            errors.append('El dominio ingresado no es valido')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            errors.append('EL correo ingresado ya esta en uso')
        return email_obj
    
class UpdatePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        label = 'Contraseña actual',
        style = {'placeholder':'Escribe tu contraseña actual', 'input_type':'password'},
        required = True,
        write_only = True
    )
    password2 = serializers.CharField(
        label = 'Contraseña nueva',
        style = {'placeholder':'Escribe tu contraseña nueva', 'input_type':'password'},
        required = True,
        write_only = True
    )
    password3 = serializers.CharField(
        label = 'Confirmar contraseña',
        style = {'placeholder':'Repite la nueva contraseña', 'input_type':'password'},
        required = True,
        write_only = True
    )
    def validate_password2(self, value):
        password_obj = value
        errors = []
        if len(password_obj)< 8:
            errors.append('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[a-zñ]', password_obj):
            errors.append('La contraseña debe tener al menos una letra minuscula')
        if not re.search(r'[A-ZÑ]', password_obj):
            errors.append('La contraseña debe tener al menos una letra mayuscula')
        if not re.search(r'[0-9]', password_obj):
            errors.append('La contraseña debe tener al menos un numero')
        if not re.search(r'[^a-zA-Z0-9ñÑ]', password_obj):
            errors.append('La contraseña debe tener al menos un caracter especial')
        if errors:
            raise    serializers.ValidationError(errors)
        return password_obj
    
    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        password3 = attrs.get('password3')
        user = self.context.get('request').user
        errors = {}
        if not user.check_password(password1):
            errors['password1']='La contraseña actual ingresada no es correcta'
        if password1 == password2:
            errors['password2']='La contraseña nueva no puede ser igual que la actual'
        if password2 != password3:
            errors['password3']='Las contraseñas no coinciden'
        if errors:
            raise serializers.ValidationError(errors)
        attrs.pop('password1')
        attrs.pop('password3')
        return attrs
    
    def update(self, instance, validated_data):
        password = validated_data['password2']
        user = instance
        user.set_password(password)
        user.save()
        return user
    
class UpdatePerfilSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )
    image = serializers.ImageField(
        label = 'Foto de perfil',
        style = {'help_text':'Solo se aceptan imagenes png', 'input_type':'file','accept':'image/png'},
        required = True
    )
    balance = serializers.ReadOnlyField()
    class Meta:
        model = Perfil
        fields = ['user','image','balance']
    def validate_image(self, value):
        image_obj = value
        allow_content = ['image/png']
        errors =[]
        if image_obj:
            if image_obj.content_type not in allow_content:
                errors.append('Formato de imagen no valido')
            if image_obj.size > 5*1024*1024:
                errors.append('Imagen demasiado grande')
            if errors:
                raise serializers.ValidationError(errors)
        return image_obj
    
    def update(self, instance, validated_data):
        perfil= instance.perfil
        perfil.image = validated_data.get('image')
        perfil.save()
        return instance
    
#########################################################################
###### VIEWSET DE GESTIÓN DE CUENTA
###### Agrupa acciones de actualización de usuario, password y perfil
#########################################################################
class UpdateUserViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'update_user':
            return UserUpdateSerializer
        if self.action == 'update_password':
            return UpdatePasswordSerializer
        return UpdatePerfilSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.action == 'update_user' or self.action == 'update_password':
            return User.objects.filter(id=self.request.user.id)
        return Perfil.objects.select_related('user').filter(user = self.request.user)
    @action (detail = False, methods = ['get','patch'], url_path='update_user')
    def update_user(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(data = request.data, instance = request.user, context={'request':request}, partial=True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'exito':'Los datos se modificaron satisfactoriamente'
            }, status= status.HTTP_200_OK
        )
    @action (detail = False, methods=['post'], url_path='update_password')
    def update_password(self, request):
        serializer = self.get_serializer(data = request.data, instance = request.user, context = {'request':request})
        serializer.is_valid(raiser_exception = True)
        serializer.save()
        return Response(
            {
                'Exito':'La contraseña se modifico satisfactoriamente'
            }, status=status.HTTP_200_OK
        )
    @action (detail = False, methods =['post'], url_path='perfil_update')
    def perfil_update(self, request):
        serializer = self.get_serializer(data = request.data, instance = request.user, context = {'request':request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'exito':'La foto de modifico',
                'image_url':request.user.perfil.image.url
            }
        )

#########################################################################
###### AUTENTICACIÓN Y TOKENS
#########################################################################

class AuthenticateSerializer(serializers.Serializer):
    username = serializers.CharField(
        label = 'Nombre de usuario',
        style = {'placeholder':'Escribe tu nombre de usuario'},
        required = True,
        write_only = True,
        trim_whitespace=True
    )
    password = serializers.CharField(
        label = 'Contraseña',
        style = {'placeholder':'Escribe tu contraseña', 'input_type':'password'},
        required = True,
        write_only = True
    )
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request = self.context.get('request')
        errors = {}
        user = authenticate(request = request, username = username, password = password)
        if not user:
            errors['username']='La contraseña o el usuario no existen'
        if not user.is_active:
            errors['username']='Cuenta bloqueada'
        if errors:
            raise serializers.ValidationError(errors)
        attrs['user']=user
        return attrs

class AuthenticateUserViewSet(viewsets.GenericViewSet):
    serializer_class = AuthenticateSerializer
    permission_classes = [Anonimouspermission]
    queryset = User.objects.all()
    @action (detail = False, methods=['post'], url_path='autenticar')
    def login(self, request):
        serializer = self.get_serializer(data = request.data, context={'request':request})
        serializer.is_valid(raise_exception = True)
        user =serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user = user)
        return Response(
            {
                'token':token.key,
                'user_id':user.id,
                'exito':'Bienvenido'
            }, status=status.HTTP_200_OK
        )
    

#########################################################################
###### VISTAS ADMINISTRATIVAS DE USUARIOS
#########################################################################
class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name','is_staff']

class FilterListUser(django_filters.FilterSet):
    username = django_filters.CharFilter(
        label = 'Buscar usuario',
        field_name='username',
        lookup_expr='icontains',
        widget = forms.TextInput(attrs={'placeholder':'Buscar usuario'})
    )
    class Meta:
        model = User
        fields = ['username']

class ListUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ListUserSerializer
    permission_classes = [StaffPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FilterListUser
    queryset = User.objects.all()


#########################################################################
###### GESTIÓN DE CATÁLOGO (PRODUCTOS, CATEGORÍAS, MARCAS)
#########################################################################

class RegisterProductoSerializet(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name_product = serializers.CharField(
        label ='Nombre del producto',
        style = {'placeholder':'Escribe el nombre de l producto'},
        required = True,
        trim_whitespace = True
    )
    category_product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar categoria',
        queryset = Category.objects.all()
    )
    brand_product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar marca',
        queryset = Brand.objects.all()
    )
    price_product = serializers.DecimalField(
        label = 'Precio',
        style = {'placeholder':'Escribe el precio del producto'},
        decimal_places= 2,
        max_digits=12,
        default = 1
    )
    stock_product = serializers.IntegerField(
        label = 'Stock',
        style = {'placeholder':'Escribe el stock actual'},
        default = 1
    )
    img_product = serializers.ImageField(
        label ='Seleccionar imagen',
        style = {'help_text':'Solo se admiten imagenes en formato png'},
    )
    class Meta:
        model = Products
        fields = ['id','name_product','category_product','brand_product','price_product','stock_product','img_product']
    
    def validate_name_product(self, value):
        product_obj = value.upper().strip()
        queryset = Products.objects.filter(name_product__iexact = product_obj)
        letter_count = 0
        errors =[]
        if len(product_obj) < 3:
            errors.append('El nombre del producto debe tener al menos 3 caracteres')
        for letter in product_obj:
            if letter.isalpha():
                letter_count+=1
        if letter_count < 2:
            errors.append('El nombre del producto debe tener al menos 2 letras')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            errors.append('El nombre del producto ingresado ya existe en la base de datos')
        if errors:
            raise serializers.ValidationError(errors)
        return product_obj
    def validate_price_product(self, value):
        price_obj = value
        errors = []
        if price_obj is None or price_obj < 1:
            errors.append('Porfavor ingrese un precio valido')
        if price_obj > 99999999:
            errors.append('Se supero el limite de precio maximo permitido')
        if errors:
            raise serializers.ValidationError(errors)
        return price_obj
    def validate_stock_product(self, value):
        stock_obj = value
        errors = []
        if stock_obj is None:
            errors.append('Porfavor ingrese un stock valido')
        if stock_obj <1:
            errors.append('El stock no puede ser menor a 1')
        if stock_obj > 99999:
            errors.append('Se supero el maximo de stock permitido')
        if errors:
            raise serializers.ValidationError(errors)
        return stock_obj
    def validate_img_product(self, value):
        img_obj = value
        allow_content = ['image/png']
        errors = []
        if img_obj:
            if img_obj.content_type not in allow_content:
                errors.append('Formato de imagen no permitido')
            if img_obj.size > 5*1024*1024 :
                errors.append('Imagen demasiado grande')
            if errors:
                raise serializers.ValidationError(errors)
        return img_obj
    
class ProductsFilterSet(django_filters.FilterSet):
    name_product = django_filters.CharFilter(
        label = 'Nombre de producto',
        field_name='name_product',
        lookup_expr='icontains',
        widget = forms.TextInput(attrs={'placeholder':'Buscar producto'})
    )
    max_price_product = django_filters.NumberFilter(
        label = 'Precio maximo',
        field_name= 'price_product',
        lookup_expr='lte',
        widget = forms.NumberInput(attrs={'placeholder':'Precio maximo'})
    )
    min_price_product = django_filters.NumberFilter(
        label = 'Precio minimo',
        field_name='price_product',
        lookup_expr='gte',
        widget = forms.NumberInput(attrs={'placeholder':'Precio minimo'})
    )
    category_product = django_filters.ModelMultipleChoiceFilter(
        label = 'Filtrar por categoria',
        field_name = 'category_product',
        queryset = Category.objects.all(),
        widget = forms.SelectMultiple()
    )
    brand_product = django_filters.ModelMultipleChoiceFilter(
        label = 'Filtrar por marca',
        field_name= 'brand_product',
        queryset = Brand.objects.all(),
        widget = forms.SelectMultiple()
    )
    class Meta:
        model = Products
        fields = ['name_product', 'max_price_product','min_price_product','category_product','brand_product']

class AdminProductViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterProductoSerializet
    def get_permissions(self):
        if self.action in ['list','retireve']:
            return [permissions.IsAuthenticated()]
        return [StaffPermission()]
    django_filters = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductsFilterSet
    queryset = Products.objects.select_related('category_product', 'brand_product').all()
    def update(self, *args, **kwargs):
        if self.action == 'update':
            return Response(
                {
                    'Error':'No se puede aplicar la petición PUT en este formulario'
                }
            )

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name_category = serializers.CharField(
        label = 'Nombre de la categoria',
        style = {'placeholder':'Escribe el nombre de la categoria'},
        required =True,
        trim_whitespace = True
    )
    class Meta:
        model = Category
        fields = ['id','name_category']
    
    def validate_name_category(self, value):
        category_obj = value.upper().strip()
        queryset = Category.objects.filter(name_category__iexact = category_obj )
        letter_count = 0
        errors = []
        if len(category_obj) < 4:
            errors.append('El nombre de categoria debe tener al menos 4 caracteres')
        if re.search(r'[^a-zA-Z\sñÑ]', category_obj):
            errors.append('El nombre de categoria no puede llevar numeros ni caracteres especiales.')
        for letter in category_obj:
            if letter.isalpha():
                letter_count += 1
        if letter_count < 4:
            errors.append('El nombre de la categoria debe tener al menos 4 letras')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            errors.append('El nombre de la categoria ingresada ya existe')
        if errors:
            raise serializers.ValidationError(errors)
        return category_obj

class AdminCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [StaffPermission]
    queryset = Category.objects.all()

class BrandSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name_brand = serializers.CharField(
        label = 'Nombre de marca',
        style = {'placeholder':'Escribe el nombre de la marca'},
        required = True,
        trim_whitespace = True
    )
    class Meta:
        model = Brand
        fields = ['id','name_brand']
    def validate_name_brand(self, value):
        brand_obj = value.upper().strip()
        queryset = Brand.objects.filter(brand_name__iexact = brand_obj)
        letter_count = 0
        errors = []
        if len(brand_obj) < 3:
            errors.append('El nombre de la marca debe tener al menos 3 caracteres')
        if re.search(r'[^a-zA-Z0-9ñÑ\s\.\-\,]', brand_obj):
            errors.append('El nombre de la marca contiene caracteres especiales no valido')
        for letter in brand_obj:
            if letter.isalpha():
                letter_count += 1
        if letter_count < 2:
            errors.append('El nombre de la marca debe tener al menos 2 letras')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            errors.append('El nombre de la marca ingresada ya existe en la base de datos')
        if errors:
            raise serializers.ValidationError(errors)
        return brand_obj

class AdminBrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = [StaffPermission]
    queryset = Brand.objects.all()


#########################################################################
###### INTERACCIÓN: VALORACIONES Y COMENTARIOS
#########################################################################

class ValorationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar producto',
        queryset = Products.objects.all()
    )
    rating = serializers.IntegerField(
        label = 'Valoración',
        style = {'placeholder':'Valorar'},
        default = 1
    )
    class Meta:
        model = valoration
        fields = ['id','user','product','rating']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset = valoration.objects.all(),
                fields = ['user','product'],
                message='No puedes valorar el mismo producto 2 veces'
            )
        ]
    def validate_rating(self, value):
        rating_obj = value
        if rating_obj is None or rating_obj <1:
            rating_obj = 1
        if rating_obj > 5:
            rating_obj = 5
        return rating_obj
    @transaction.atomic
    def create(self, validated_data):
        instance_valoration = super().create(validated_data)
        product_select = validated_data.get('product')
        product_stats = valoration.objects.filter(product = product_select).aggregate(total = Avg('rating'))
        product_total_valoration = product_stats.get('total') or 0
        product_select.valoration = round(product_total_valoration, 2)
        product_select.save()
        return instance_valoration

class AdminValoration(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ValorationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = valoration.objects.all()
    
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.HiddenField(default = serializers.CurrentUserDefault())
    datetime = serializers.DateTimeField(label = 'Fecha')
    name_user = serializers.ReadOnlyField(source = 'username.username')
    product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar producto',
        queryset = Products.objects.all()
    )
    comment = serializers.CharField(
        label = 'Comentario',
        style = {'placeholder' : 'Escribe tu comentario'},
        required = True,
        trim_whitespace = True
    )
    class Meta:
        model = Comments
        fields = ['username','datetime','name_user','product','comment']
    def validate_comment(self, value):
        comment_obj = value.strip()
        if len(comment_obj) < 5:
            raise serializers.ValidationError('Comentario demasiado corto')
        return comment_obj

class AdminCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comments.objects.select_related('user','product').all()


#########################################################################
###### SISTEMA DE CARRITO DE COMPRAS
###### Modelos y serializadores para la persistencia del carrito
#########################################################################
#####CART MODEL
class CartModel(models.Model):
    user = models.OneToOneField(Settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    at_created = models.DateTimeField(default = timezone.now)
@property
def total_price(self):
    calculator = self.items.all().aggregate(total = Sum(F('quantity') * F('product__price_product')))
    results = calculator.get('total') or 0
    total = round(results, 2)
    return total
####CART MODEL ITEM
class CartModelItem(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['cart', 'product'],
                name = 'UniqueItemCart'
            )
        ]
    @property
    def subtotal(self):
        return self.quantity * self.product.price_product


####CART ITEM SERIALIZER
class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        label = 'Seleccionar producto',
        queryset = Products.objects.all()
    )
    quantity = serializers.IntegerField(
        label = 'Cantidad',
        default = 1,
        allow_null = False)
    subtotal = serializers.ReadOnlyField()
    class Meta:
        model = CartModelItem
        fields = ['product', 'quantity', 'subtotal']
    def validated_quantity(self, value):
        quantity_obj = value
        if quantity_obj is None or quantity_obj < 1:
            quantity_obj = 1
        if quantity_obj > 99:
            quantity_obj = 99
        return quantity_obj
    def create(self, validated_data):
        user = self.context.get('request').user
        user_cart = CartModel.objects.get_or_create(user = user)
        new_product = validated_data.get('product')
        cart_instance = Cart.objects.filter(product = new_product, cart = user_cart).first()
        if cart_instance:
            cart_instance.quantity = validated_data.get('quantity')
            cart_instance.save()
            return cart_instance
        validated_data['cart'] = user_cart
        return super().create(validated_data)
####CART SERIALIZER
class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    cart = CartItemSerializer(many = True, read_only = True, source = 'items')
    total_price = serializers.ReadOnlyField()
    class Meta:
        model = CartModel
        fields = ['user', 'cart', 'total_price','created_at']