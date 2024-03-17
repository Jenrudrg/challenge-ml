from datetime import datetime
import xlsxwriter
from io import BytesIO
from admin_soft.models import SaleDetail

def generate_xlsx():
    # Crear un libro y una hoja
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    hoja = workbook.add_worksheet()

    # Definir los formatos
    formato_titulo = workbook.add_format({'bold': True, 'font_size': 14})
    formato_cabecera = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black'})
    
    number_format = workbook.add_format({'num_format': '#,##0.00', 'text_wrap': True, 'valign': 'top'})
    wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top', 'align': 'right'})
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})


    # Escribir el título
    date_now = datetime.now().strftime("%Y-%m-%d")
    hoja.write('A1', f'Listado de Ventas {date_now}', formato_titulo)

    # Escribir las cabeceras
    hoja.write('A3', 'Folio Venta', formato_cabecera)
    hoja.write('B3', 'Fecha', formato_cabecera)
    hoja.write('C3', 'Creado por?', formato_cabecera)
    hoja.write('D3', 'Product', formato_cabecera)
    hoja.write('E3', 'Cantidad', formato_cabecera)
    hoja.write('F3', 'Total', formato_cabecera)


    hoja.autofilter('A3:F3')


    # Escribir los datos
    sales = [sale_prod for sale_prod in SaleDetail.objects.all().order_by("-id")]

    fila = 2
    for sale in sales:
        sale: SaleDetail = sale
        fila += 1
        hoja.write(fila, 0, str( sale.sale.uuid), wrap_format)
        hoja.write(fila, 1, sale.sale.created_at.date(), date_format)
        hoja.write(fila, 2, sale.sale.created_user.username, wrap_format)
        hoja.write(fila, 3, sale.product.name, wrap_format)
        hoja.write(fila, 4, sale.quantity, wrap_format)
        hoja.write(fila, 5, sale.quantity * sale.product.price , number_format)

    # Ajustar el ancho de las columnas
    hoja.set_column('A:A', 30)
    hoja.set_column('B:B', 30)
    hoja.set_column('C:C', 30)
    hoja.set_column('D:D', 30)
    hoja.set_column('E:E', 30)
    hoja.set_column('F:F', 30)

    # Cerrar el libro
    workbook.close()

    return output
