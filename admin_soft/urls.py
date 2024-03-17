from django.urls import path
from admin_soft import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('productos/', views.productos, name='productos'),
    path('ventas/', views.ventas, name='ventas'),
    path('compras/', views.compras, name='compras'),
    path('download_sales/', views.download_sales, name='download_sales'),

    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

]
