from admin_soft.models import Product, SaleDetail


def save_sale(request, sale):
    total_sale = 0

    for key, value in request.POST.items():
        if key.startswith('product_'):
            if 'id' in key:
                producto_id = value
            if 'quantity' in key:
                quantity = value
            
                # Calcular el total
                product = Product.objects.get(pk=producto_id)
                total = product.price * int(quantity)
                total_sale += total

                # Crear el SaleDetail y asociarlo a la venta
                SaleDetail.objects.create(
                    sale=sale,
                    product_id=producto_id,
                    quantity=quantity,
                    total=total
                )
    sale.total = total_sale
    sale.save()
        