import django_filters, re
from django import forms
from .models import Perfil, Products, Category, Brand
from django.contrib.auth.models import User

class UserUsernameFilters(django_filters.FilterSet):
    #USERNAME
    username = django_filters.CharFilter(
        label = 'Buscar usuario',
        field_name='username',
        lookup_expr='icontains',
        widget = forms.TextInput(attrs={'placeholder':'Buscar usuario'}),
        method= 'filter_by_length'
    )

    #FIRST NAME FILTER
    first_name = django_filters.CharFilter(
        label = 'Buscar por nombre',
        field_name='first_name',
        lookup_expr='icontains',
        widget = forms.TextInput(attrs={'placeholder':'Buscar nombre'}),
        method='filter_by_length'
    )
    #LAST NAME FILTER
    last_name = django_filters.CharFilter(
        label = 'Buscar por apellido',
        field_name='last_name',
        lookup_expr='icontains',
        widget = forms.TextInput(attrs={'placeholder':'Buscar apellido'}),
        method='filter_by_length'
    )
    #STAFF FILTER
    is_staff = django_filters.BooleanFilter(
        label = 'Filtrar por permisos por',
        field_name='is_staff',
        widget = forms.Select(choices=[
            (False, 'usuarios'),
            (True, 'Administradores'),
            ('', 'todos'),
        ])
    )
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'is_staff']
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.strip()
        return username
    def filter_by_length(self,queryset, name, value):
        if value:
            if len(value)>2:
                filters_obj = {f'{name}__icontains':value}
                return queryset.filter(**filters_obj)
            return queryset.none()
        return queryset
    



###################################################
####################PRODUCTS FILTERS###############
###################################################

class ProductFilterSet(django_filters.FilterSet):
    Nombre_producto = django_filters.CharFilter(
        label = 'Buscar Product',
        field_name='name_product',
        lookup_expr='icontains',
        widget = forms.TextInput(attrs={'placeholder':'Buscar producto'})
    )
    Maximo = django_filters.NumberFilter(
        label = 'Precio Maximo',
        field_name='price_product',
        lookup_expr='lte',
        widget = forms.NumberInput(attrs={'placeholder':'Precio maximo'})
    )
    Minimo = django_filters.NumberFilter(
        label = 'Precio minimo',
        field_name='price_product',
        lookup_expr='gte',
        widget = forms.NumberInput(attrs={'placeholder':'Precio minimo'})
    )
    Categoria = django_filters.ModelMultipleChoiceFilter(
        label = 'Filtrar por categoria',
        field_name='category_product',
        queryset = Category.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )
    Marca = django_filters.ModelMultipleChoiceFilter(
        label = 'Filtrar marcas',
        field_name= 'brand_product',
        queryset = Brand.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Products
        fields = ['Nombre_producto', 'Categoria', 'Minimo','Maximo']
