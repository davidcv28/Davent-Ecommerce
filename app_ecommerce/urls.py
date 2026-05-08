from django import urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import userviewset, productviewset, cartviewset
from . import views
###API ROUTER###
router = DefaultRouter()
###############################################################
################USERS ROUTERS VIEWSET############################
###############################################################

###########################
####STAFF USER VIEWSETS####
###########################

#REGISTER ADMIN VIEWSET
router.register(r'registro_usuarios_admin', userviewset.RegisterAdminViewSet, basename='Administrador-usuarios')
#LIST USER  VIEWSET
router.register(r'lista_usuarios', userviewset.ListUserViewSet, basename='listado-usuarios')
############################
##NORMAL USER VIEWSETS######
############################
#REGISTER VIEWSET
router.register(r'registro_usuarios', userviewset.RegisterUserViewSet, basename='Registro-usuarios')
#UPDATE VIEWSET
router.register(r'user_update', userviewset.UpdateUserViewSet,  basename='update_user')
#LOGIN VIEWSET
router.register(r'', userviewset.AuthenticateUserViewSet, basename = 'iniciar sesión')
#LIST VIEWSET


###############################################################
################PRODUCTS ROUTERS VIEWSETS############################
###############################################################

####STAFF PRODUCT VIEWSET
#REGISTER PRODUCT VIEWSET
router.register(r'administrador_productos', productviewset.RegisterProductViewSet, basename='Administrador_productos')

#REGISTER CATEGORY VIEWSET
router.register(r'administrador_categorias', productviewset.RegisterCategoryViewSet, basename='Administrador_categorias')
#REGISTER BRAND VIEWSET
router.register(r'administrador_marcas', productviewset.RegisterBrandViewSet, basename='Administrador_marcas')
#REGISTER VALORATION VIEWSET
router.register(r'administrador_valoración', productviewset.RegisterValorationViewSet, basename='Administrador_valoración')
#REGISTER COMMENT VIEWSET
router.register(r'comentarios', productviewset.RegisterCommentsViewSet, basename='Administrador_comentarios')

###############################################################
################CART ROUTERS VIEWSETS############################
###############################################################
#LIST CART VIEWSET
router.register(r'carrito', cartviewset.CartListViewSet, basename='Carrito')
#CART ITEM REGISTER VIEWSET
router.register(r'agregar_carrito', cartviewset.CartItemRegisterViewSet, basename='Agregar_carrito')
#CART DETAIL ITEMS VIEWSET

urlpatterns = [
    path('',views.home, name="home"),
    #LOGIN VIEWS
    path('inicio_sesión/', views.login_view, name ='login'),
    path('registrarse/', views.login_register, name = 'register'),
    path('registro__exitoso/', views.register__success, name = 'register__success'),
    #ADMIN
    path('administrador_sistema/', views.admin_view, name = 'admin-view'),
    #PRODUCTS VIEWS
    path('productos/', views.products, name = 'products'),
    path ('productos/producto/<int:id>', views.product__view, name='product' ),
    #BUY CART
    path('agregar_item/<int:id>', views.add__item__cart, name = "add___item__cart"),
    path ('eliminar_item/<int:id>', views.delete__item__cart, name="delete__item__cart"),
    path('incrementar_carrito/', views.increment__item__cart, name = "increment__item__cart"),
    path('decrementar_carrito/', views.decrement__item__cart, name= "decrement__item__cart"),
    path('incrementar_carrito_view/', views.increment__item__viewcart, name = "increment__item__viewcart"),
    path('decrementar_carrito_view/', views.decrement__item__viewcart, name = "decrement__item__viewcart"),
    path('incrementar_decrementar_carrito_view_movil/', views.increment_decrement__item__viewcart__movil, name = "increment_decrement__item__viewcart__movil"),
    path ('carrito_de_compras/', views.buycart_view, name="buycart"),
    #INVOICE
    path('factura/<int:id>', views.invoice_view, name= "invoice__view"),
    #USER MENU
    path('menu_usuario/', views.user_menu, name="user menu"),
    path('guardar_perfil/', views.change__perfil__user, name='update_perfil'),
    path('guardar_datos/', views.change__details__user, name = "update_details_user"),
    path('cerrar_sesión/', views.salir, name ="logout"),
]
# API URLs

urlpatterns += [
    path('api/', include(router.urls)),
    
]
