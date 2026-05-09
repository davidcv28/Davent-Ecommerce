from app_ecommerce.models import Products, Category, Brand
from django.core.management import BaseCommand
from django.conf import settings
from django.core.files import File
import os

"""

En este modulo cargaremos los productos de prueba para el ecommerce

"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        ###CATEGORY LOAD
        list_category = ['CHOCOLATE', 'CARAMELO', 'ALFAJOR', 'CHICLE']
        list_category_add = []
        for category in list_category:
            category_item = Category(name_category = category)
            list_category_add.append(category_item)
        Category.objects.bulk_create(list_category_add, ignore_conflicts=True)
        ###BRAND LOAD
        list_brand = ['CANELA', 'DULCE VIDA', 'CHICLAMON','CHOCOLITO']
        list_brand_add = []
        for brand in list_brand:
            brand_item  = Brand(name_brand = brand)
            list_brand_add.append(brand_item)
        Brand.objects.bulk_create(list_brand_add, ignore_conflicts = True)
        #####MAP CATEGORY AND BRAND
        all_categories =  Category.objects.all()
        map_category = {c.name_category : c for c in all_categories}
        all_brands = Brand.objects.all()
        map_brand = {b.name_brand : b for b in all_brands}
        ####PRODUCTS LOAD
        media_img = os.path.join(settings.BASE_DIR, 'media', 'productos' )
        dict_products = {
                            'alfajor_canela':{
                                'name_product':'ALFAJOR CANELA 50G.',
                                'stock':200,
                                'price_product':3000,
                                'category_product':map_category['ALFAJOR'],
                                'brand_product' : map_brand['CANELA'],
                                'img_product' : os.path.join(media_img, 'alfajor_canela.png')
                            },
                            'alfajor_dulce_vida':{
                                'name_product':'ALFAJOR DULCE VIDA 50G.',
                                'stock':500,
                                'price_product':2500,
                                'category_product':map_category['ALFAJOR'],
                                'brand_product' : map_brand['DULCE VIDA'],
                                'img_product' : os.path.join(media_img, 'alfajor_dulce_vida.png')
                            },
                            'chicle_chiclamon':{
                                'name_product':'CHICLE CHICLAMON.',
                                'stock':1500,
                                'price_product':500,
                                'category_product':map_category['CHICLE'],
                                'brand_product' : map_brand['CHICLAMON'],
                                'img_product' : os.path.join(media_img, 'chicle_chiclamon.png')
                            },
                            'chocolate_chocolito':{
                                'name_product':'CHOCOLATE CHOCOLINO 100GR.',
                                'stock':300,
                                'price_product':5500,
                                'category_product':map_category['CHOCOLATE'],
                                'brand_product' : map_brand['CHOCOLINO'],
                                'img_product' : os.path.join(media_img, 'chocolate_chocolino.png')
                            }
                        }
        list_add_product = []
        for key,product in dict_products.items():
            try:
                with open(product['img_product'], 'rb') as p:
                    product_item, created = Products.objects.get_or_create(name_product = product['name_product'], defaults={
                        'stock_product': product['stock'],
                        'price_product' : product['price_product'],
                        'category_product' : product['category_product'],
                        'brand_product' : product['brand_product'],
                        'img_product' : File(p)
                    }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"SE CARGO EL PRODUCTO {product['name_product']}"))
            except:
                return