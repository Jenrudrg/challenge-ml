from admin_soft.models import Purchase, PurchaseDetail

def save_purchase(request, purchase):
    total_purchase = 0

    for key, value in request.POST.items():
        if key.startswith('product_'):
            if 'id' in key:
                producto_id = value
            if 'quantity' in key:
                quantity = value
            if 'price' in key:
                price = value
            
                # Calcular el total
                total = float(price) * int(quantity)
                total_purchase += total

                # Crear el SaleDetail y asociarlo a la venta
                PurchaseDetail.objects.create(
                    purchase=purchase,
                    product_id=producto_id,
                    quantity=quantity,
                    purchase_price=price,
                    total=total
                )
    
    purchase.total = total_purchase
    purchase.save()
        