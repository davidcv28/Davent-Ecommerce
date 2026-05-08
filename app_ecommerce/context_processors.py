from . import cart


#CART CONTEXT
def cart_content(request):
    Cart = cart.buy__cart(request)
    return{
        'Cart':Cart,
        'total__quantity':Cart.total_quantity,
        'total__price': Cart.total_price,
        'iva__price':Cart.iva_price,
        'total__iva':Cart.total_iva
    }