#APLICACION
#creo este archivo para gestionar mis urls de la aplicacion porque
#puedo tener varias urls

from django.urls import path
from .import views

urlpatterns = [
    path('',views.RenderbusquedaProductoHome, name="busquedaProducto") ,  
#Renderizacion de paginas
    path('ListadoProducto/',views.ListadoProducto, name="vistaProducto") ,
#plantilla busqueda Producto
    path('registrarNombreProducto/',views.registrarNombreProducto) ,
    path('registrarNombreProducto/eliminarNombreProducto/<idnombreproducto>',views.eliminarNombreProducto, name="busquedaProducto"),
#plantilla vistaIDProducto
    path('ListadoPorID/<idnombreproducto>',views.ListadoPorID, name="vistaIDProducto") ,  

]
