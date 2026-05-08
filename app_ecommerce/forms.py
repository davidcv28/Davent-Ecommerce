
from django import forms
from .models import Products, Category, Brand, Comments, Perfil
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.files.uploadedfile import UploadedFile 


#/////////////////////////////////////////////
#//////////FORMULARIOS PARA USUARIO ////////
#////////////////////////////////////////////

#########################################################################
###### FORMULARIO DE LOGIN (AUTENTICACIÓN)
#########################################################################
class form__login(AuthenticationForm):
   username = forms.CharField( max_length= 254, widget= forms.TextInput(attrs={'class':'input__container--input', 'placeholder':'Nombre de usuario', 'id':'login__user'}) )
   password=forms.CharField( max_length=255, widget=forms.PasswordInput(attrs={'class':'input__container--input', 'placeholder':'Contraseña', 'id':'login__password'}) )


#########################################################################
###### FORMULARIO DE REGISTRO (CREACIÓN DE CUENTA)
###### Extiende UserCreationForm para incluir datos personales
#########################################################################
class form__register(UserCreationForm):
   first_name = forms.CharField( max_length=255,widget=forms.TextInput(attrs={'class':'input__container--input','placeholder':'Nombre'}))
   last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'input__container--input', 'placeholder':'Apellido'}))
   email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'class':'input__container--input','placeholder':'Correo electronico'}))
   class Meta(UserCreationForm.Meta):
      model = UserCreationForm.Meta.model
      fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['username'].widget.attrs.update({'class':'input__container--input', 'placeholder':'Nombre de usuario'})

      self.fields['password1'].widget.attrs.update({'class':'input__container--input','placeholder':'Contraseña'})
      
      self.fields['password2'].widget.attrs.update({'class':'input__container--input','placeholder':'Repetir contraseña'})

#########################################################################
###### EDITOR DE DATOS PERSONALES
###### Incluye validaciones personalizadas para nombres y dominios de email
#########################################################################
class form__userupdate(forms.ModelForm):
   class Meta:
      model = User
      fields = ['first_name', 'last_name', 'email']
      widgets= {
         'first_name': forms.TextInput(attrs={'class':'input__updateform textbox','placeholder':'Nombre', 'required': 'true'}),
         'last_name': forms.TextInput(attrs={'class':'input__updateform textbox','placeholder':'Apellido', 'required': 'true'}),
         'email': forms.EmailInput(attrs={'class':'input__updateform textbox','placeholder':'Correo', 'required': 'true'}),
      }
      
   def clean_first_name(self):
      first_name = self.cleaned_data.get('first_name')
      if len(first_name) < 4 or len(first_name) >60:
         raise forms.ValidationError('El nombre debe tener miminamente 4 caracteres y como maximo 60')
      return first_name
   def clean_last_name(self):
      last_name = self.cleaned_data.get('last_name')
      if len(last_name) < 3 or len(last_name) >60:
         raise forms.ValidationError('El Apellido debe tener miminamente 3 caracteres y como maximo 60')
      return last_name
   def clean_email(self):
      email = self.cleaned_data.get('email')
      domain_valids = ['@gmail.com', '@outlook.com', '@hotmail.com', '@yahoo.com']
      contain_domain= False
      for domain in domain_valids:
         if email.endswith(domain):
            contain_domain = True
      if contain_domain == False:
         raise forms.ValidationError('El dominio del correo electronico no es valido')
      return email

#########################################################################
###### ACTUALIZACIÓN DE PERFIL (IMAGEN)
###### Valida extensiones permitidas para la foto de perfil
#########################################################################
class perfil_updateform(forms.ModelForm):
   class Meta:
      model = Perfil
      fields = ['image']
      widgets = {
         'image': forms.FileInput(attrs={'class':'file__input', 'placeholder':'Seleccionar imagen', 'accept':'image/png,image/jpeg,image/x-icon', 'id':'image__update__fileinput', 'required': 'true', 'hidden': 'true' }),
      }
   def clean_image(self):
      image =self.cleaned_data.get('image')
      allow__extensions = ['.ico', '.png', '.jpg']
      extension__valid = False
      for img__select in allow__extensions:
         if image.name.lower().endswith(img__select):
            extension__valid =True
      if not extension__valid:
         raise forms.ValidationError('El formato de la imagen seleccionada no esta permitido')
      return image
      
#########################################################################
###### FORMULARIO SECUNDARIO DE ACTUALIZACIÓN
###### Basado en UserChangeForm para gestión administrativa
#########################################################################
class form__user__update(UserChangeForm):
   class Meta:
      model= User
      fields =['first_name', 'last_name', 'username', 'email']

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['first_name'].widget.attrs.update({'class':'input__container--input','placeholder':'Nombre'})
      self.fields['first_name'].required = True
      self.fields['last_name'].widget.attrs.update({'class':'input__container--input','placeholder':'Apellido'})
      self.fields['username'].widget.attrs.update({'class':'input__container--input','placeholder':'Nombre de usuario'})
      self.fields['email'].widget.attrs.update({'class':'input__container--input','placeholder':'Correo electronico'})



#/////////////////////////////////////////////
#//////////FORMULARIOS PARA PRODUCTO ////////
#////////////////////////////////////////////

#########################################################################
###### GESTIÓN DE PRODUCTOS
###### Centraliza la lógica de validación de stock, precios e imágenes
#########################################################################
class products_form(forms.ModelForm):
   class Meta:
      model= Products
      fields=['name_product', 'brand_product', 'category_product','stock_product', 'price_product','img_product']
      widgets={
         'name_product': forms.TextInput(attrs={'class':'input__container--input', 'placeholder':'Nombre producto', 'id':'product__name'}),
         'brand_product': forms.Select(attrs={'class':' selectbox', 'placeholder':'Marca', 'id':'product__brand'}),
         'category_product': forms.Select(attrs={'class':' selectbox', 'placeholder':'Categoria', 'id':'product__category'}),
         'stock_product': forms.NumberInput(attrs = {'class':'input__container--input', 'placeholder':'Stock', 'id':'product__stock'}),
         'price_product': forms.NumberInput(attrs={'class':'input__container--input', 'placeholder':'Precio del producto', 'id':'product__price'}),
         'img_product': forms.FileInput(attrs={'class':'input__container--input', 'placeholder':'Selecciona imagen', 'id':'product__img', 'accept':'image/png'})
      }

   ###########################################
   ###### LÓGICA DE VALIDACIÓN DE CAMPOS
   ###########################################
   def clean_name_product(self):
      name_product = self.cleaned_data.get('name_product').upper()
      letter__count = 0
      
      if len(name_product) < 4:
         raise forms.ValidationError('El nombre del producto debe tener minimamente 4 caracteres')
      for i in name_product:
            if i.isalpha():
               letter__count += 1
      if letter__count < 4:
         raise forms.ValidationError('El nombre del producto debe tener al menos 4 letras')
      return name_product

   def clean_stock_product(self):
      stock_product = self.cleaned_data.get('stock_product')
      if stock_product is not None and stock_product < 1 :
         raise forms.ValidationError('El stock no puede ser menor que 1')
      return stock_product

   def clean_price_product(self):
      price_product = self.cleaned_data.get('price_product')
      if price_product is not None and price_product < 1:
          raise forms.ValidationError('El precio es demasiado bajo')
      return price_product

   def clean_img_product(self):
      img_product = self.cleaned_data.get('img_product')
      allowed_types = ['image/png']
      if img_product and isinstance(img_product, UploadedFile):
         if img_product.size > 5 * 1024 * 1024 :
            raise forms.ValidationError('El tamaño de la imagen es demasiado grande')
         if img_product.content_type not in allowed_types:
            raise forms.ValidationError('Solo se aceptan imagenes de formato PNG')
      return img_product

   def clean(self):
      super().clean()
      name_product = self.cleaned_data.get('name_product')
      brand_product = self.cleaned_data.get('brand_product')
      queryset = Products.objects.filter(name_product = name_product, brand_product = brand_product)
      if self.instance and self.instance.pk:
         queryset =queryset.exclude(pk=self.instance.pk)
      
      if queryset.exists():
         raise forms.ValidationError('El producto ya existe')
      return self.cleaned_data





#/////////////////////////////////////////////
#//////////FORMULARIOS PARA MARCAS   ////////
#////////////////////////////////////////////

#########################################################################
###### REGISTRO DE MARCAS
###### Valida unicidad y longitud mínima
#########################################################################
class form__brand__register(forms.ModelForm):
   class Meta:
      model = Brand
      fields=['name_brand']
      widgets={
         'name_brand': forms.TextInput(attrs={'class':'input__container--input', 'placeholder':'Nombre de Marca', 'id':'name__brand'})
      }
   def clean_name_brand(self):
      name_brand = self.cleaned_data.get('name_brand').upper()
      if not name_brand :
         raise forms.ValidationError('El campo esta vacio')
      if len(name_brand)<4:
         raise forms.ValidationError('El nombre de la marca es demasiado corto')
      if Brand.objects.filter(name_brand = name_brand).exists():
         raise forms.ValidationError('El nombre de la marca ya existe')
      return name_brand
   
#/////////////////////////////////////////////
#//////////FORMULARIOS PARA CATEGORIAS   ////////
#////////////////////////////////////////////

#########################################################################
###### REGISTRO DE CATEGORÍAS
###### Normaliza a mayúsculas y verifica duplicados
#########################################################################
class form__category__register(forms.ModelForm):
   class Meta:
      model = Category
      fields = ['name_category']
      widgets ={
         'name_category': forms.TextInput(attrs={'class':'input__container--input', 'placeholder':'Nombre de categoria', 'id':'name__category'})
      }
   def clean_name_category(self):
      name_category = self.cleaned_data.get('name_category').upper()
      if not name_category:
         raise forms.ValidationError('Porfavor escriba el nombre de la categoria')
      if len(name_category) < 4:
         raise forms.ValidationError('El nombre de la categoria es demasiado corto')
      if Category.objects.filter(name_category = name_category).exists():
         raise forms.ValidationError('La categoria ingresada ya existe')
      
      return name_category
   
#//////////////////////////////////////////////////
#//////////FORMULARIOS PARA COMENTARIOS   ////////
#/////////////////////////////////////////////////

#########################################################################
###### SISTEMA DE COMENTARIOS
###### Controla la longitud máxima para evitar saturación de la BD
#########################################################################
class create__comment__form(forms.ModelForm):
   class Meta:
      model = Comments
      fields = ['comment']
      widgets ={
         'comment': forms.Textarea(attrs={'class':'input__container--input', 'placeholder':'Escribe tu comentario...', 'id':'comments__coment'})
      }
   
   def clean_comment(self):
      comment = self.cleaned_data.get('comment')
      if not comment:
         raise forms.ValidationError('Porfavor escriba el comentario')
      if len(comment) > 2500:
         raise forms.ValidationError('el comentario no puede tener mas de 2500 caracteres')
      return comment
