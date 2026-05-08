from django.shortcuts import render, redirect, get_object_or_404
from .models import Products, Category, Brand, Comments, valoration, Perfil, Pucharse_order_detail, Pucharse_order
from django.contrib.auth.decorators import login_required
from .forms import form__login, form__register, form__user__update, products_form, form__brand__register, form__category__register, create__comment__form, form__userupdate, perfil_updateform
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from .cart import buy__cart
from django.db.models import F 

#HOME VIEW#
def home(request):
    products = Products.objects.all()
    return render (request, 'home.html', {'products':products})

##################################################
#################LOGIN VIEW ######################
##################################################
def login_view (request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            login__form = form__login(request, data = request.POST)
            if login__form.is_valid():
                username = login__form.cleaned_data['username']
                password = login__form.cleaned_data['password']
                user = authenticate(request, username = username, password = password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'El usuario o contraseña no son correctos')
            else:
                messages.error(request, 'El usuario o contraseña no son correctos')
        else:
            login__form = form__login()
        return render (request, 'login/login.html', {'login__form':login__form})


def login_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        register_form = form__register(request.POST)
        if register_form.is_valid():
            register_form.save()
            
            return redirect('register__success')
    else:
        register_form=form__register()
    return render (request, 'login/register.html', {'register__form':register_form})


def register__success(request):
    if request.user.is_authenticated:
        return render (request, 'home.html')
    else:
        return render(request, 'login/register_success.html')


###ADMIN VIEW###
login_required(login_url='/')
def admin_view(request):
    #USERS FORMS AND MODEL
    formregister = form__register()
    formupdateuser = form__user__update(prefix='user__update__modal')
    users__admin = User.objects.all()
    user__id__input = request.POST.get('id__update__user')
    #PRODUCTS FORMS AND MODEL
    product__form = products_form()
    products__admin = Products.objects.all()
    product__title__msj = ''
    product__button__msj = ''
    #BRANDS FORMS
    brandformregister = form__brand__register()
    brand__msj__error = False
    category__success = request.GET.get('category__success','')
    #CATEGORY FORM
    categoryformregister = form__category__register()
    category__msj__error = False
    brand__success =request.GET.get('brand__success','')
    ####SECTION AND ERRORS#####
    error__msj = False
    if brand__success:
        error__msj=True
    if category__success:
        error__msj = True
    update__msj__error= False
    section__page = request.GET.get('section_page', 'user__view' )

    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'GET':
        user_search_filter = request.GET.get('search__input__user','')
        product__search__filter = request.GET.get('search__input__product', '')
        if user_search_filter:
            users__admin = users__admin.filter(username__icontains=user_search_filter)
        if product__search__filter:
            products__admin=products__admin.filter(name_product__icontains = product__search__filter)
        
    elif request.method == 'POST':
        form__type = request.POST.get('form__type')
        #USERS FORMS ACTIONS
        username__input=request.POST.get('username__input')
        if form__type == 'add__user':
            formregister = form__register(request.POST)
            if formregister.is_valid():
                formregister.save()
                return redirect (f"{request.path}?section_page={section__page}")
            else:
                error__msj=True
        if form__type =='delete__user':
            username__input=get_object_or_404(User,username=username__input)
            username__input.delete()
            return redirect(f"{request.path}?section_page={section__page}")
        if form__type =='update__user':
            user = get_object_or_404(User, id=user__id__input)
            formupdateuser=form__user__update(request.POST , instance=user, prefix='user__update__modal')
            if formupdateuser.is_valid():
                formupdateuser.save()
                return redirect(f"{request.path}?section_page={section__page}")
            else:
                update__msj__error=True
        #PRODUCTS FORMS ACTIONS
        if form__type == 'add__product':
            product__form= products_form(request.POST, request.FILES)
            if product__form.is_valid():
                product__form.save()
                return redirect (f"{request.path}?section_page={section__page}")
            else:
                error__msj=True
                product__title__msj = 'Registro de producto'
                product__button__msj = 'Registrar producto'
        if form__type == 'delete__product':
            product__id__input = request.POST.get('product__id__input')
            product__delete__select = get_object_or_404(Products, id=product__id__input)
            product__delete__select.delete()
            return redirect(f"{request.path}?section_page={section__page}")
        if form__type == 'update__product':
            product__id__input = request.POST.get('id__product__input','')
            product = get_object_or_404(Products, id=product__id__input)
            product__form = products_form(request.POST, request.FILES, instance=product)
            if product__form.is_valid():
                product__form.save()
                return redirect(f"{request.path}?section_page={section__page}")
            else:
                error__msj = True
                product__title__msj = 'Editor de producto'
                product__button__msj = 'Guardar cambios'
        #BRAND FORM ACTION
        if form__type == 'add__brand':
            brandformregister = form__brand__register(request.POST)
            if brandformregister.is_valid():
                brandformregister.save()
                return redirect (f"{request.path}?section_page={section__page}&brand__success=True")
            else:
               
                brand__msj__error = True
                
        #CATEGORY FORM ACTION
        if form__type == 'add__category':
            categoryformregister = form__category__register(request.POST)
            if categoryformregister.is_valid():
                categoryformregister.save()
                return redirect(f"{request.path}?section_page={section__page}&category__success=True")
            else:
                
                category__msj__error = True
            

    return render (request, 'admin/admin.html',
    {#USERS PANEL
    'users__admin':users__admin,'formreguser':formregister, 'update__user__id':user__id__input,
    'form__user__update':formupdateuser ,
    #PRODUCTS PANEL
    'products__admin':products__admin,'product__form':product__form,
    'brandformregister':brandformregister,'brand__success':brand__success, 'brand__msj__error':brand__msj__error,
    'categoryformregister':categoryformregister,'category__success':category__success,'category__msj__error':category__msj__error,
    'product__title__msj':product__title__msj, 'product__button__msj':product__button__msj,
    #ERRORS MSJ AND SECTION PAGE
    'section__page':section__page, 'error__msj':error__msj, 'update__error__msj':update__msj__error})



    
 

##################################################
#################PRODUCTS VIEW ###################
##################################################

## PRODUCTS VIEW ##
def products(request):
    brands = Brand.objects.all()
    categorys = Category.objects.all()
    products_model = Products.objects.all()
    valorations_model = valoration.objects.all()    
    if request.method == 'GET':
        list_category = request.GET.getlist('category__item')
        list_brand = request.GET.getlist('brand__item')
        price_order = request.GET.get('price__item','')
        input_search = request.GET.get('input_search','')
        if len(list_category) != 0:
            products_model = products_model.filter(category_product__name_category__in = list_category)
        if len(list_brand) != 0:
            products_model=products_model.filter(brand_product__name_brand__in=list_brand)
        if input_search:
            products_model = products_model.filter(name_product__icontains = input_search)
        if price_order != '':
            if price_order == 'Mayor precio':
                products_model=products_model.order_by('-price_product')
            else:
                products_model= products_model.order_by('price_product')
           
    return render (request, 'products/products.html', {'products':products_model, 'categorys':categorys, 'brands':brands, 'valorations_model':valorations_model})

## PRODUCT VIEW ##
def product__view(request, id):
    product_item = get_object_or_404(Products, id=id)
    category__product = product_item.category_product
    related_products = Products.objects.filter(category_product=category__product).exclude(id=product_item.id)
    valorations__product = valoration.objects.filter(product = product_item)
    valoration__total__count = valorations__product.count()
    valoration__buttons = True 
    if request.user.is_authenticated:
            if valoration.objects.filter(product = product_item, user = request.user).exists():
                valoration__buttons=False
    if not product_item:
        return redirect('products')
    comments = Comments.objects.filter(product = id)
    comment__form = create__comment__form()
    if request.method == 'POST':
        type__action = request.POST.get('type__action')
        valoration__stars = request.POST.get('rating')
        
        if type__action == 'create__comment':
            comment__form = create__comment__form(request.POST)
            if comment__form.is_valid():
                new__comment = comment__form.save(commit=False)
                new__comment.product = product_item
                new__comment.username = request.user
                new__comment.save() 
                if valoration__stars and int(valoration__stars) > 0 and int(valoration__stars) < 6:
                    valoration.objects.create(
                        product = product_item,
                        user = request.user,
                        rating = valoration__stars
                    ) 
                    valoration__total__sum__query = valorations__product.aggregate(Sum('rating'))
                    valoration__total__sum = valoration__total__sum__query['rating__sum']
                    valoration__total__count = valoration.objects.filter(product = product_item).count()
                    valoration__total = valoration__total__sum / valoration__total__count
                    product_item.valoration_product = valoration__total
                    product_item.save()
                    return redirect('product', id=id)

        
    return render(request,'products/product.html', {'product':product_item,'related_products':related_products, 'comment__form':comment__form, 'comments':comments, 'valoration__buttons':valoration__buttons, 'valoration__total__count':valoration__total__count, 'valoration__model':valorations__product} )


###################################
############# BUY CART ############
###################################
@login_required(login_url='/')
def add__item__cart (request, id):
    if request.method == 'POST':
        product = get_object_or_404(Products, id=id)
        quantity_product = int(request.POST.get('quantity__product'))
        cart_user = buy__cart(request)
        cart_user.add_item(product, quantity_product)
        return render(request , 'partials/products_partials/buycart.html')
@login_required(login_url='/')    
def delete__item__cart(request,id):
    if request.method == 'POST':
        product = get_object_or_404(Products, id= id)
        cart_user = buy__cart(request)
        cart_user.delete_item(product)
        return render (request, 'partials/products_partials/buycart.html')
@login_required(login_url='/')
def increment__item__cart(request):
    if request.method == 'POST':
        get_product = request.POST.get("id_product")
        product = get_object_or_404(Products, id=get_product)
        user_cart = buy__cart(request)
        user_cart.increment_item(product)
        return render (request, "partials/products_partials/buycart2.html")
@login_required(login_url='/')
def decrement__item__cart(request):
    if request.method == 'POST':
        get_product = request.POST.get("id_product")
        product = get_object_or_404(Products, id=get_product)
        user_cart = buy__cart(request)
        user_cart.decrement_item(product)
        return render (request, "partials/products_partials/buycart2.html")

    



    
            
    
    
    
########################################
############# BUY CART  VIEW############
########################################
@login_required(login_url='/')
def buycart_view(request):
    user_cart = buy__cart(request)
    if not  user_cart.cart.items():
        return redirect('home')
    if request.method == 'POST':
            action_type= request.POST.get('type__action')
            if action_type == 'pucharse__action':
                pucharse__total = user_cart.total_price()
                price__iva = user_cart.iva_price()
                total_price_iva = user_cart.total_iva()
                if total_price_iva <= request.user.perfil.balance:
                    order = Pucharse_order.objects.create(order_user = request.user, order_total = pucharse__total, iva = price__iva,  order_total_price = total_price_iva)
                    for item in user_cart.cart.values():
                        Pucharse_order_detail.objects.create(detail_order =order, detail_product = get_object_or_404(Products, id = item['product_id']), detail_quantity = item['product_quantity'], detail_price = item['product_price'], detail_total = item['product_total_price'])
                    Perfil.objects.filter(user = request.user).update(balance = F('balance') - pucharse__total)
                    user_cart.clear()
                    pucharse__id = order.id
                    return redirect('invoice__view', pucharse__id)
                else:
                    messages.error(request, 'Saldo insuficiente en la cuenta')
                    
            if action_type == 'delete__action':
                product__select = request.POST.get('product__delete')
                product = get_object_or_404(Products, id=product__select)
                user_cart.delete_item(product)
                if not user_cart.cart.items():
                    return redirect('home')
                else:
                    return redirect(f'{request.path}')
    return render (request, 'products/buycart_view.html')
@login_required(login_url='/')
def increment__item__viewcart(request):
    if request.method == 'POST':
        product_get = request.POST.get("id_product")
        product = get_object_or_404(Products, id=product_get)
        cart_user = buy__cart(request)
        cart_user.increment_item(product)
        return render (request, "partials/products_partials/buycartview_post.html")
@login_required(login_url='/')    
def decrement__item__viewcart(request):
    if request.method =='POST':
        get__id__product = request.POST.get("id_product")
        product = get_object_or_404(Products, id=get__id__product)
        cart_user = buy__cart(request)
        cart_user.decrement_item(product)
        return render (request, "partials/products_partials/buycartview_post.html")
@login_required(login_url='/')
def increment_decrement__item__viewcart__movil(request):
    if request.method == 'GET':
        user_cart = buy__cart(request) 
        product__select = request.GET.get('item__select')
        product = get_object_or_404(Products, id=product__select)
        action__type = request.GET.get('type__action')
        if action__type == "decrement":
            user_cart.decrement_item(product)
        else:
            user_cart.increment_item(product)
    return render (request, 'partials/products_partials/buycartview_post_movil.html')      

 ####################################################
 ############ INVOICE VIEW #########################
 # #################################################
@login_required(login_url='/')
def invoice_view (request, id):
    invoice = get_object_or_404(Pucharse_order, id = id)
    if invoice.order_user != request.user:
        return redirect('home')
    details = Pucharse_order_detail.objects.filter(detail_order = invoice.id)
    return render (request, 'products/invoice.html', {'invoice':invoice, 'details':details})
    

########################################
############# USER MENU     ############
########################################
@login_required(login_url='/')
def user_menu(request):
    user_details__valorations = valoration.objects.filter(user=request.user).count()
    select_option = request.GET.get('select_option')
    #FORMULARIOS DE LA VIEW DETAILS__ACCOUNT
    user_updateform = form__userupdate(instance=request.user)
    user_perfilupdate = perfil_updateform(instance=request.user.perfil)
    user_pucharse_items = Pucharse_order.objects.filter(order_user = request.user.id)
    if request.method == 'GET':
        if not select_option:
            select_option ='main__info'
    return render (request, 'user_menu/menu.html', {'user__details__valorations': user_details__valorations, 'select_option': select_option,
    #FORMS Y VARIABLES DETAIL ACCOUNT
    'user__updateform': user_updateform, 'user__perfilupdate':user_perfilupdate,
    #FORM Y VARIABLES PUCHARSES_DETAIL
    'user_pucharses_items':user_pucharse_items})
@login_required(login_url='/')
def change__perfil__user(request):
    if request.method =='POST':
         user_updateform = perfil_updateform(request.POST, request.FILES,  instance=request.user.perfil)
         if  user_updateform.is_valid():
            user_updateform.save()
    else:
         user_updateform = perfil_updateform(instance= request.user.perfil)
    return render (request, 'partials/user_menu/user_update_image.html', {'user__perfilupdate': user_updateform})
@login_required(login_url='/')
def change__details__user(request):
    if request.method == 'POST':
        user_updateform = form__userupdate(request.POST, instance=request.user)
        if user_updateform.is_valid():
            user_updateform.save()
    return render (request, 'partials/user_menu/user_update_details.html', {'user__updateform':user_updateform})


@login_required(login_url='/')
def salir(request):
    logout(request)
    return render (request, 'home.html')
