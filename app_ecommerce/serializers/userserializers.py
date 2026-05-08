from rest_framework import serializers, validators
from rest_framework.validators import UniqueValidator
from ..models import Products, Category, Brand, valoration, Comments, Perfil, Cart
from django.contrib.auth.models import User
from django.db import transaction
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth import authenticate, get_user_model
import re, os
    
#######################################################
###############ADMINS SERIALIZERS######################
#######################################################

#########################################################################
###### REGISTRO DE ADMINISTRADORES (STAFF)
###### Incluye validaciones estrictas de seguridad para perfiles internos
#########################################################################
class RegisterAdminSerializer(serializers.ModelSerializer):
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
    email = serializers.EmailField(
        label = 'Correo electronico',
        style = {'placeholder':'Escribe tu correo electronico', 'input_type':'email'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    username = serializers.CharField(
        label = 'Nombre de usuario',
        style = {'placeholder':'Escribe tu nombre de usuario'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    password = serializers.CharField(
        label = 'Contraseña',
        style = {'placeholder':'Escribe tu contraseña', 'input_type':'password'},
        required = True,
        write_only = True,   
    )
    password2 = serializers.CharField(
        label = 'Confirmar contraseña',
        style = {'placeholder':'Confirmar contraseña', 'input_type':'password'},
        required = True,
        write_only = True,   
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'username','password','password2','is_staff']
    def validate_first_name(self, value):
        name_obj = value.upper().strip()
        letter_count = 0
        errors = []
        if re.search(r'[^a-zA-Z\sñÑ]', name_obj):
            errors.append('Solo se admiten letras')
        for letter in name_obj:
            if letter.isalpha():
                letter_count += 1
        if letter_count < 3:
            errors.append('El nombre debe tener al menos 3 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return name_obj
    def validate_last_name(self, value):
        last_name_obj = value.upper().strip()
        letter_count = 0
        errors = []
        if re.search(r'[^a-zA-Z\sñÑ]', last_name_obj):
            errors.append('Solo se admiten letras')
        for letter in last_name_obj:
            if letter.isalpha():
                letter_count +=1
        if letter_count < 3:
            errors.append('El apellido debe llevar al menos 3 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return last_name_obj
    def validate_email(self, value):
        email_obj = value.strip()
        queryset = User.objects.filter(email__iexact = email_obj)
        domain_exist = False
        allow_domains = ['@hotmail.com', '@gmail.com','@yahoo.com','@outlook.com','@live.com']
        errors = []
        for domain in allow_domains:
            if email_obj.lower().endswith(domain):
                domain_exist = True
                break
        if not domain_exist:
            errors.append('Dominio ingresado no valido')
        if self.instance:
            queryset = queryset.exclude(pk= self.instance.pk)
        if queryset.exists():
            errors.append('El correo ingresado ya se encuentra vinculado a una cuenta')
        if errors:
            raise serializers.ValidationError(errors)
        return email_obj
    def validate_username(self, value):
        username_obj = value.strip()
        queryset = User.objects.filter(username__iexact = username_obj)
        errors = []
        if re.search(r'[^a-zA-Z0-9ñÑ]', username_obj):
            errors.append('No se admiten espacios ni caracteres especiales')
        if len(username_obj) < 6:
            errors.append('El nombre de usuario debe tener al menos 6 caracteres')
        if self.instance:
            queryset = queryset.exclude(pk = self.instance.pk)
        if queryset.exists():
            errors.append('El nombre de usuario ingresado ya existe')
        if errors:
            raise serializers.ValidationError(errors)
        return username_obj
    def validate_password(self, value):
        password_obj = value
        errors = []
        if len(password_obj) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[a-z]', password_obj):
            errors.append('La contraseña debe tener al menos una letra minuscula')
        if not re.search(r'[A-Z]', password_obj):
            errors.append('La contraseña debe tener al menos una letra mayuscula')
        if not re.search(r'[0-9]', password_obj):
            errors.append('La contraseña debe tener al menos un numero')
        if not re.search(r'[^a-zA-Z0-9]', password_obj):
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
        return attrs
    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password'],
            is_staff = validated_data.pop('is_staff', False)
        )
        Cart.objects.create(user = user)
        return user


#########################################################################
###### SERIALIZADOR DE LISTADO DE USUARIOS
###### Vista simplificada para paneles de administración
#########################################################################
class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','username']

#######################################################
###############USERS SERIALIZERS######################
#######################################################

#########################################################################
###### REGISTRO DE USUARIOS FINALES (CLIENTES)
###### Automatiza la creación del carrito de compras tras el registro
#########################################################################
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
    email = serializers.EmailField(
        label = 'Correo electronico',
        style = {'placeholder':'Escribe tu correo electronico', 'input_type':'email'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    username = serializers.CharField(
        label = 'Nombre de usuario',
        style = {'placeholder':'Escribe tu nombre de usuario'},
        required = True,
        write_only = True,
        trim_whitespace = True
    )
    password = serializers.CharField(
        label = 'Contraseña',
        style = {'placeholder':'Escribe tu contraseña', 'input_type':'password'},
        required = True,
        write_only = True,   
    )
    password2 = serializers.CharField(
        label = 'Confirmar contraseña',
        style = {'placeholder':'Confirmar contraseña', 'input_type':'password'},
        required = True,
        write_only = True,   
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'username','password','password2']
    def validate_first_name(self, value):
        name_obj = value.upper().strip()
        letter_count = 0
        errors = []
        if re.search(r'[^a-zA-Z\sñÑ]', name_obj):
            errors.append('Solo se admiten letras')
        for letter in name_obj:
            if letter.isalpha():
                letter_count += 1
        if letter_count < 3:
            errors.append('El nombre debe tener al menos 3 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return name_obj
    def validate_last_name(self, value):
        last_name_obj = value.upper().strip()
        letter_count = 0
        errors = []
        if re.search(r'[^a-zA-Z\sñÑ]', last_name_obj):
            errors.append('Solo se admiten letras')
        for letter in last_name_obj:
            if letter.isalpha():
                letter_count +=1
        if letter_count < 3:
            errors.append('El apellido debe llevar al menos 3 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return last_name_obj
    def validate_email(self, value):
        email_obj = value.strip()
        queryset = User.objects.filter(email__iexact = email_obj)
        domain_exist = False
        allow_domains = ['@hotmail.com', '@gmail.com','@yahoo.com','@outlook.com','@live.com']
        errors = []
        for domain in allow_domains:
            if email_obj.lower().endswith(domain):
                domain_exist = True
                break
        if not domain_exist:
            errors.append('Dominio ingresado no valido')
        if self.instance:
            queryset = queryset.exclude(pk= self.instance.pk)
        if queryset.exists():
            errors.append('El correo ingresado ya se encuentra vinculado a una cuenta')
        if errors:
            raise serializers.ValidationError(errors)
        return email_obj
    def validate_username(self, value):
        username_obj = value.strip()
        queryset = User.objects.filter(username__iexact = username_obj)
        errors = []
        if re.search(r'[^a-zA-Z0-9ñÑ]', username_obj):
            errors.append('No se admiten espacios ni caracteres especiales')
        if len(username_obj) < 6:
            errors.append('El nombre de usuario debe tener al menos 6 caracteres')
        if self.instance:
            queryset = queryset.exclude(pk = self.instance.pk)
        if queryset.exists():
            errors.append('El nombre de usuario ingresado ya existe')
        if errors:
            raise serializers.ValidationError(errors)
        return username_obj
    def validate_password(self, value):
        password_obj = value
        errors = []
        if len(password_obj) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[a-z]', password_obj):
            errors.append('La contraseña debe tener al menos una letra minuscula')
        if not re.search(r'[A-Z]', password_obj):
            errors.append('La contraseña debe tener al menos una letra mayuscula')
        if not re.search(r'[0-9]', password_obj):
            errors.append('La contraseña debe tener al menos un numero')
        if not re.search(r'[^a-zA-Z0-9]', password_obj):
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
        return attrs
    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password'],
        )
        Cart.objects.create(user = user)
        return user

#########################################################################
###### ACTUALIZACIÓN DE DATOS PERSONALES
###### Permite modificar Nombre, Apellido y Email con validación de dominio
#########################################################################
class UpdateUserSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(
        label = 'Nombre',
        style = {'placeholder':'Escribe tu nombre'},
        required = True,
        trim_whitespace = True,
    )
    last_name = serializers.CharField(
        label = 'Apellido',
        style = {'placeholder':'Escribe tu apellido'},
        required = True,
        trim_whitespace = True
    )
    email = serializers.EmailField(
        label = 'Correo electronico',
        style = {'placeholder':'Escribe tu correo', 'input_type':'email'},
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
        if re.search(r'[^a-zA-Z\sñÑ]', name_obj):
            errors.append('Solo se admiten letras')
        for letter in name_obj:
            if letter.isalpha():
                letter_count += 1
        if letter_count < 3:
            errors.append('El nombre debe tener al menos 3 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return name_obj
    def validate_last_name(self, value):
        last_name_obj = value.upper().strip()
        letter_count = 0
        errors = []
        if re.search(r'[^a-zA-Z\sñÑ]', last_name_obj):
            errors.append('Solo se admiten letras')
        for letter in last_name_obj:
            if letter.isalpha():
                letter_count +=1
        if letter_count < 3:
            errors.append('El apellido debe llevar al menos 3 letras')
        if errors:
            raise serializers.ValidationError(errors)
        return last_name_obj
    def validate_email(self, value):
        email_obj = value.strip()
        queryset = User.objects.filter(email__iexact = email_obj)
        domain_exist = False
        allow_domains = ['@hotmail.com', '@gmail.com','@yahoo.com','@outlook.com','@live.com']
        errors = []
        for domain in allow_domains:
            if email_obj.lower().endswith(domain):
                domain_exist = True
                break
        if not domain_exist:
            errors.append('Dominio ingresado no valido')
        if self.instance:
            queryset = queryset.exclude(pk= self.instance.pk)
        if queryset.exists():
            errors.append('El correo ingresado ya se encuentra vinculado a una cuenta')
        if errors:
            raise serializers.ValidationError(errors)
        return email_obj

#########################################################################
###### CAMBIO DE CONTRASEÑA
###### Verifica la password anterior y la fortaleza de la nueva
#########################################################################
class UpdatePasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        label = 'Contraseña actual',
        style={'placeholder':'Escribe tu contraseña actual', 'input_type':'password'},
        required = True,
        write_only = True
    )
    new_password = serializers.CharField(
        label = 'Contraseña Nueva',
        style={'placeholder':'Escribe tu contraseña Neuva', 'input_type':'password'},
        required = True,
        write_only = True
    )
    repeat_password = serializers.CharField(
        label = 'Confirmar contraseña',
        style={'placeholder':'Repite la nueva contraseña', 'input_type':'password'},
        required = True,
        write_only = True
    )
    def validate_old_password (self, value):
        old_password_obj = value
        errors = []
        user= self.context.get('request').user
        if not user.check_password(old_password_obj):
            errors.append('La contraseña actual no es correcta')
        if errors:
            raise serializers.ValidationError(errors)
        return old_password_obj
    def validate_new_password (self, value):
        new_password_obj = value
        errors = []
        if len(new_password_obj) < 8:
            errors.append('La nueva contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[a-z]', new_password_obj):
            errors.append('La nueva contraseña debe tener al menos una letra minuscula')
        if not re.search(r'[A-Z]', new_password_obj):
            errors.append('La nueva contraseña debe tener al menos una letra mayuscula')
        if not re.search(r'[0-9]', new_password_obj):
            errors.append('La nueva contraseña debe tener al menos un numero')
        if not re.search(r'[^a-zA-Z0-9]', new_password_obj):
            errors.append('La nuevo contraseña debe tener al menos un caracter especial (ej. @)')
        if errors:
            raise serializers.ValidationError(errors)
        return new_password_obj
    def validate (self, attrs):
        new_password_obj = attrs.get('new_password')
        repeat_password_obj = attrs.get('repeat_password')
        old_password_obj = attrs.get('old_password')
        errors = {}
        if new_password_obj == old_password_obj:
            errors['new_password'] = 'La nueva contraseña no puede ser la misma que la actual'
        if new_password_obj != repeat_password_obj:
            errors['repeat_password']='Las contraseñas no coinciden'
        if errors:
            raise serializers.ValidationError(errors)
        attrs.pop('old_password')
        attrs.pop('repeat_password')
        return  attrs
    def update(self, instance, validated_data):
        new_password_obj = validated_data.get('new_password')
        instance.set_password(new_password_obj)
        instance.save()
        return instance

#########################################################################
###### AUTENTICACIÓN DE USUARIO
###### Valida credenciales y estado de la cuenta (activo/inactivo)
#########################################################################
class UserAuthenticatedSerializer(serializers.Serializer):
    username = serializers.CharField(
        label = 'Nombre de usuario',
        style = {'placeholder':'Escribe tu nombre de usuario'},
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
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request = self.context.get('request')
        errors =[]
        user = authenticate(request = request, username= username ,  password=password)
        if not user:
            errors.append('La cuentra ingresada no existe')
        if not user.is_active:
            errors.append('La cuenta se encuentra desactivada')
        if errors:
            raise serializers.ValidationError(errors)
        attrs['user']=user
        return attrs
    

#########################################################################
###### ACTUALIZACIÓN DE MULTIMEDIA (PERFIL)
###### Gestión de archivos de imagen con límites de formato y tamaño
#########################################################################
class PerfilUpdateSerializer(serializers.Serializer):
    image = serializers.ImageField(
        label = 'foto de perfil',
        style = {'input_type':'file', 'help_text':'Solo se admiten imagenes en formato .png','accept':'image/png','required':'required'},
        required = True,
        allow_null=False,       
    )
    def validate_image(self, value):
        image_obj = value
        allow_content = ['image/png', 'image/jpeg']
        errors = []
        if image_obj:
            if image_obj.content_type not  in allow_content:
                errors.append('Formato de imagen no valido, solo se acepta png y jpeg')
            if image_obj.size > 5*1024*1024:
                errors.append('Imagen demasiado grande')
            if errors:
                raise serializers.ValidationError(errors)
        return image_obj
    def update(self,instance, validated_data):
        perfil = instance.perfil
        perfil.image = validated_data.get('image')
        perfil.save()
        return instance
