

# calcular stock dinámico de todos los productos
# se suma por las compras y se resta por las ventas

from admin_soft.models import Product, Purchase, Sale, PurchaseDetail


def all_stock():
    """
        Retorna un diccionario con el stock dinámico de todos los productos
    """
    products = Product.objects.all()
    stock = {}

    for product in products:
        stock[product.id] = {
        'name': product.name,
        'stock': 0
        }

        # Compras
        purchases = PurchaseDetail.objects.filter(product=product)
        for purchase in purchases:
            stock[product.id]['stock'] += purchase.quantity

        # Ventas
        ventas = Sale.objects.all()
        for venta in ventas:
            detalles = venta.sale_detail.filter(product=product)
            for detalle in detalles:
                stock[product.id]['stock'] -= detalle.quantity
    
    return stock