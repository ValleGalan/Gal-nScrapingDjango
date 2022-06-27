from django.shortcuts import render, redirect
from django.contrib import messages
#importo las clases con las que trabajo
from .models import Producto,NombreProducto
#Subconsultas en django
from django.db.models import Q  
# Para web scraping
import requests
from bs4 import BeautifulSoup  #libreria para realizar el raspado
import string   #usar funciones de string
 
baseURL = 'https://listado.mercadolibre.com.ar/'

#Renderizacion de plantillas__________________________________________
#Se pasa toda la lista de NombreProducto y se la ordena por idnombreproducto para mostrar
#en la plantilla busquedaProducto.html
def RenderbusquedaProductoHome(request):    
    nombreListado = NombreProducto.objects.all().order_by('idnombreproducto')   
    return render(request, "busquedaProducto.html",{"nombreproductos": nombreListado})
#Plantilla vista Producto _______________________________________________________________
#Se pasa toda la lista de Producto para mostrarla en la plantilla vistaProducto.html
def ListadoProducto(request):   
    productosListado = Producto.objects.all()
    return render(request, "vistaProducto.html", {"productosListado": productosListado})

#Plantilla vistaIDProducto _______________________________________________________________
#Se pasa por parametro el idnombreproducto para filtrarlo , se compara que sea ese mismo id
#si no vieran datos en la tabla Producto entonces se muestra una notificacion de 
#no hay fatos sino se para el context con el listado y se renderiza en vistaIDProducto.html
def ListadoPorID(request,idnombreproducto): #Filtra por id
    productosListado = Producto.objects.filter(idnombreproducto=idnombreproducto)
    validarHayDatos=productosListado.count()
    if validarHayDatos==0:
        messages.success(request, 'No hay datos!')
    context = {'productosListado': productosListado } #pasa el listado de los datos filtrados      
    return render(request, "vistaIDProducto.html", context) 

# Plantilla busqueda Producto _________________________________________________
def registrarNombreProducto(request):
    nombre=request.POST['productoInputBuscar']   #palabra a buscar

    if NombreProducto.objects.filter( nombre =nombre): #Existe el nombre buscado en la tabla
        messages.success(request, 'Ya existe el producto')

        print("AQUI SE HACE EL WEB SCRAPING SI LA PALABRA YA SE BUSCO Y EXISTE") 
        #Web scraping 
        final_url = baseURL + nombre        
        response = requests.get(final_url)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')

        lista = soup.find_all('li', {'class': "ui-search-layout__item"})
        for item in lista[0:15]:   
            item_titulo = item.find('h2',class_= "ui-search-item__title").text
            item_url = item.find("a", "ui-search-link").get("href")

            productoDetalle = BeautifulSoup(requests.get(item_url).text,'html.parser')
            item_precio = productoDetalle.find('span','andes-money-amount__fraction').string.replace(".", "")
            if (item_precio==" "):
                item_precio="0"
            item_imagen = item.find('img','ui-search-result-image__element').get('data-src')

            #Transformar a string
            nombre_titulo = str(item_titulo)
            precio_nuevo = str(item_precio)
           
            #Obtener el id de la tabla NombreProducto para pasarcela a la tabla Producto
        idnombreproducto=NombreProducto.objects.last() 
         
         #Lista los nombres buscados pero sin agregar porque ya existe    
        nombreListado = NombreProducto.objects.all()

        #Comparar el precio si se modifico 
        if Producto.objects.filter(nombre_producto =nombre_titulo):
            #Precio subio
                if Producto.objects.filter( Q(precio__gt=precio_nuevo) & Q( idnombreproducto=idnombreproducto)):
                    productosActualizadosListado= Producto.objects.filter(nombre_producto =nombre_titulo)
                    messages.success(request, 'El precio subio en Mercado Libre, fijese en la "Tabla del producto que se modifico el precio" ' )                       
                    return render(request,'busquedaProducto.html',{"nombreproductos": nombreListado,'productosActualizadosListado':productosActualizadosListado}) 
              
            #Precio No se modifico
                if Producto.objects.filter(precio =precio_nuevo).filter( idnombreproducto=idnombreproducto): 
                    print('no hay cambios')
            #Precio bajo
                elif  Producto.objects.filter( Q(precio__lt=precio_nuevo) & Q(idnombreproducto=idnombreproducto)):#
                    productosActualizadosListado= Producto.objects.filter(nombre_producto =nombre_titulo)
                    messages.success(request, 'El precio bajo en Mercado Libre, fijese en la "Tabla del producto que se modifico el precio"')
                    return render(request,'busquedaProducto.html',{"nombreproductos": nombreListado,'productosActualizadosListado':productosActualizadosListado})                   
  
        return render(request,'busquedaProducto.html',{"nombreproductos": nombreListado}) 
    else :
        print("AQUI SE HACE EL WEB SCRAPING SI SE BUSCA LA PALABRA POR PRIMERA VEZ") 
        #Creo el nombre en la BD   
        nombreProd = NombreProducto.objects.create(nombre=nombre)

        #Lista los nombres buscados y agrega el nuevo nombre que se busco  
        nombreListado = NombreProducto.objects.all() 

        #web scraping _____________________________________________________________

        final_url = baseURL + nombre        #concatena mi url base + inpurBuscar  
        response = requests.get(final_url)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')

        lista = soup.find_all('li', {'class': "ui-search-layout__item"}) 

        for item in lista[0:15]: 
            item_titulo = item.find('h2',class_= "ui-search-item__title").text
            item_url = item.find("a", "ui-search-link").get("href") 

            productoDetalle = BeautifulSoup(requests.get(item_url).text,'html.parser')
            item_precio = productoDetalle.find('span','andes-money-amount__fraction').string.replace(".", "")
    
            if (item_precio==" "):
                item_precio="0"
            item_imagen = item.find('img','ui-search-result-image__element').get('data-src')

            #Transformar a string
            nombre_titulo = str(item_titulo)
            precio = str(item_precio)
            url_producto = str(item_url)
            url_img_producto = str(item_imagen)

            #Obtener el id de la tabla NombreProducto para pasarcela a la tabla Producto
            idnombreproducto=NombreProducto.objects.last() 

            #Guardar en la BD  
            producto = Producto.objects.create(
            idnombreproducto=idnombreproducto,
            nombre_producto=nombre_titulo,
            precio=precio,
            url_producto=url_producto,
            url_img_producto=url_img_producto)
       
        messages.success(request, 'Nombre del Producto registrado!')
        return render(request,'busquedaProducto.html',{"nombreproductos": nombreListado})  
#Funcion eliminar: se le pasa el parametro idnombreproducto que es por el cual lo filtra
# y con delete() lo borra y muestra un mensaje de que el producto se elimino
# si borra el nombre del producto tambien se borran sus datos del scraping ya que esta vinculado por
# idnombreproducto ambas tablas
def eliminarNombreProducto(request, idnombreproducto):
    producto = NombreProducto.objects.filter(idnombreproducto=idnombreproducto).delete()
    messages.success(request, 'producto eliminado!')
    return redirect("/")
 
 
'''
             #etiquetaPrecio= item.find('span','price-tag-amount')
            #item_precio = item.find('span','price-tag-fraction').string.replace(".", "") 
 '''