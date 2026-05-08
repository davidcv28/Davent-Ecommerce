### BUY CART ###

class buy__cart:
    def __init__(self,request):
       self.session = request.session
       if not 'cart' in self.session:
           self.session['cart'] = {}
       self.cart = self.session['cart']

    #CART SAVE
    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    #CART CLEAR
    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
        self.cart = {}

    #CART DELETE ITEM
    def delete_item(self, product):
        product_id = str(product.id)
        if product_id in self.cart :
            del self.cart[product_id]
            self.save()
    
    #CART ADD_ITEM
    def add_item (self,product,quantity):
        product_id = str(product.id)
        if  quantity >= 1 and quantity < 100:
            if not product_id in self.cart:
                self.cart[product_id] = {
                    'product_id': product.id,
                    'product_name': product.name_product,
                    'product_image': product.img_product.url,
                    'product_quantity': quantity,
                    'product_price':float(product.price_product),
                    'product_total_price':float(product.price_product) * quantity
                }
                self.save()
            else:
                self.cart[product_id]['product_quantity'] = quantity
                self.cart[product_id]['product_total_price'] = float(product.price_product) * quantity
                self.save()
        elif quantity == 0 and product_id in self.cart:
                del self.cart[product_id]
                self.save()
    
    #INCREMENT CART
    def increment_item(self,product):
        try:
            product_id = str(product.id)
            if product_id in self.cart:
                if self.cart[product_id]['product_quantity'] < 100:
                    self.cart[product_id]['product_quantity'] += 1
                    self.cart[product_id]['product_total_price'] += float(product.price_product)
                    self.save()
        except (TypeError, ValueError) as e:
            print(f"{e}")
    
    #DECREMENT CART
    def decrement_item(self,product):
        product_id = str(product.id)
        if  product_id in self.cart:
            if self.cart[product_id]['product_quantity'] >1:
                self.cart[product_id]['product_quantity'] -= 1
                self.cart[product_id]['product_total_price'] -= float(product.price_product)
                self.save()

    #TOTAL QUANTITY CART
    def total_quantity(self):
        total = 0
        for item in self.cart.values():
            total += item['product_quantity']
        return total
    
    #TOTAL PRICE CART
    def total_price(self):
        total=0
        for item in self.cart.values():
            total += float(item['product_total_price'])
        return total
    
    #IVA PRICE
    def iva_price(self):
        total = 0
        for item in self.cart.values():
            total += float(item['product_total_price'])
        total= total * 0.21
        return total
    
    #TOTAL PRICE + IVA
    def total_iva(self):
        subtotal = 0 
        for item in self.cart.values():
            subtotal += float(item['product_total_price'])
        iva = subtotal * 0.21
        total = subtotal + iva
        return total
    

    ####API METHOD######
    def api_get_all(self):
        return{
            'items': list(self.cart.items),
            'total_quantity': self.total_quantity,
            'total_price': self.total_price,
            'iva_price': self.iva_price(),
            'total_iva': self.total_iva,
        }