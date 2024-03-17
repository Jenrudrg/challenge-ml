from io import BytesIO
import uuid
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import LoginView
from admin_soft.forms.forms import LoginForm, ProductForm
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q, Sum
from django.db import transaction
from datetime import datetime

# Security
from django.contrib.auth.decorators import login_required

from admin_soft.models import Product, Purchase, Sale, SaleDetail
from admin_soft.utilities.reportes_xlsx import generate_xlsx
from admin_soft.utilities.save_purchase import save_purchase
from admin_soft.utilities.save_sale import save_sale
from admin_soft.utilities.paginador import paginar_registros
from admin_soft.utilities.stock import all_stock


# Create your views here.

# Pages
@login_required(login_url='/accounts/login/')
def index(request):

  ventas_por_dia_mes_actual = []
  ventas_por_dia_mes_anterior = []

  # Ventas del mes actual
  ventas_mes_actual = Sale.objects.filter(date__month=datetime.now().month)
  for i in range(1, 32):
    ventas_por_dia_mes_actual.append(ventas_mes_actual.filter(date__day=i).count())

  # Ventas del mes anterior
  ventas_mes_anterior = Sale.objects.filter(date__month=datetime.now().month-1)
  for i in range(1, 32):
    ventas_por_dia_mes_anterior.append(ventas_mes_anterior.filter(date__day=i).count())

  # Top 10 productos más vendidos
  label_top_10 = []
  data_top_10 = []
  top_10 = SaleDetail.objects.values('product__name').annotate(total=Sum('quantity')).order_by('-total')[:10]
  for i in top_10:
    label_top_10.append(i['product__name'])
    data_top_10.append(i['total'])

  print(top_10)

  context = { 
    'segment': 'Inicio',
    'ventas_por_dia_mes_actual': ventas_por_dia_mes_actual,
    'ventas_por_dia_mes_anterior': ventas_por_dia_mes_anterior,
    'label_top_10': label_top_10,
    'data_top_10': data_top_10,
   }

  return render(request, 'pages/index.html', context)

@login_required(login_url='/accounts/login/')
def productos(request):

  if request.POST:
    product_id = request.POST.get('product_id')

    if product_id:
        # Actualización de registro existente
        registro = get_object_or_404(Product, pk=product_id)
        form = ProductForm(request.POST, request=request, instance=registro)
        success_message = "Producto actualizado correctamente."
        error_message = f"Error al actualizar el productos. {form.errors}"
    else:
        # Creación de un nuevo registro
        form = ProductForm(request.POST, request=request)
        success_message = "Producto guardado correctamente."
        error_message = f"Error al guardar el Producto. {form.errors}"

    if form.is_valid():
        form.save()
        registro = form.instance


        messages.success(request, success_message)
    else:
        messages.error(request, error_message)

    return redirect('/productos')



  qs_products = Product.objects.all()

  # GET Busquedas
  if request.GET.get('search', None) is not None:
    search = request.GET.get('search')

    if search == '':
        return redirect('/productos')
    else:
        qs_products = Product.objects.filter(
                              Q(name__icontains=str(search)) |
                              Q(description__icontains=str(search)) |
                              Q(price__icontains=str(search))
                              )
  # Paginar products
  products = paginar_registros(request, qs_products, 20)

  # Formularios de Edicion de Inventario
  formularios = {}
  for i in products:
    formularios[i.id] = ProductForm(instance=i)

  qs = {
    'products': products,
  }

  context = {
    'segment': 'Productos',
    'form': ProductForm(),
    'formularios': formularios,
    'stock': all_stock()
  }
  return render(request, 'pages/productos.html', {**context, **qs})
                
@login_required(login_url='/accounts/login/')
def ventas(request):

  if request.POST:
    
    #Crear nueva venta
    try:
      with transaction.atomic():
        sale = Sale.objects.create(uuid=uuid.uuid4(), 
                                   date=request.POST.get('date'),
                                   created_user_id=request.user.id, 
                                   modifier_user_id=request.user.id)
        save_sale(request=request, sale=sale)
        messages.success(request, "Venta creada correctamente.")
    except Exception as e:
      print(f"Error al crear la venta: {e}")
      messages.error(request, f"Error al crear la venta: {e}")
    
    redirect('/ventas/')

  qs_sales = Sale.objects.all()

  # GET Busquedas
  if request.GET.get('search', None) is not None:
    search = request.GET.get('search')

    if search == '':
        return redirect('/ventas')
    else:
        qs_sales = Product.objects.filter(
                              Q(uuid__icontains=str(search)) 
                              )
  # Paginar sales
  sales = paginar_registros(request, qs_sales, 20)

  qs = {
    'sales': sales,
    'products': Product.objects.all(),
  }

  context = {
    'segment': 'Ventas',
    'stock': all_stock()
  }

  return render(request, 'pages/ventas.html', {**context, **qs})

@login_required(login_url='/accounts/login/')
def compras(request):

  if request.POST:
    #Crear nueva compra
    try:
      with transaction.atomic():
        purchase = Purchase.objects.create(uuid=uuid.uuid4(), created_user_id=request.user.id, 
                                   modifier_user_id=request.user.id)
        save_purchase(request=request, purchase=purchase)
        messages.success(request, "Compra creada correctamente.")
    except Exception as e:
      print(f"Error al crear la compra: {e}")
      messages.error(request, f"Error al crear la compra: {e}")
    
    redirect('/compras/')

  qs_purchases= Purchase.objects.all()

  # GET Busquedas
  if request.GET.get('search', None) is not None:
    search = request.GET.get('search')

    if search == '':
        return redirect('/compras/')
    else:
        qs_purchases= Purchase.objects.filter(
                              Q(uuid__icontains=str(search)) 
                              )
  # Paginar sales
  purchases= paginar_registros(request, qs_purchases, 20)


  qs = {
    'purchases': purchases,
    'products': Product.objects.all(),
  }

  context = {
    'segment': 'Compras',
  }
  return render(request, 'pages/compras.html',  {**context, **qs})


@login_required(login_url='/accounts/login/')
def download_sales(request):
    
    resultado_en_memoria: BytesIO = generate_xlsx()

    # Obtener los datos del resultado en memoria
    resultado_en_memoria.seek(0)
    datos_resultado = resultado_en_memoria.getvalue()

    resultado_en_memoria.close()

    # Crear una respuesta HTTP con el contenido del archivo
    date_now = datetime.now().strftime("%Y-%m-%d")
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="lista_ventas_{date_now}.xlsx"'
    response.write(datos_resultado)

    return response
# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')


