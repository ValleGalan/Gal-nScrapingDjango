#Se creo para generar datos y llenar la tabla de modo ramdom 
#para testear que hace el crud basico y poder comparar precios
#SOLO TESTEO NADA MAS
import os
import time
import django,random as rd
from random import random
#llamo a setting
os.environ.setdefault("DJANGO_SETTINGS_MODULE","MeliScraping.settings")

django.setup()
#importo la clase Producto de la aplicacion creada
from Aplicacion.webscraping.models import Producto

vocals = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'y', 'z',
              'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z']

def generate_string(length):
    if length <= 0:
        return False

    random_string =  ''

    for i in range(length):
        decision = rd.choice(('vocals','consonants'))

        if random_string[-1:].lower() in vocals:
            decision = 'consonants'
        if random_string[-1:].lower() in consonants:
            decision = 'vocals'
        
        if decision == 'vocals':
            character = rd.choice(vocals)
        else:
            character = rd.choice(consonants)
        
        random_string += character
    
    return random_string

def generate_number():
    return int(random()*10+1)

def generate_producto(count):
    productos = []
    for j in range(count):
        print(f'Generando Producto #{j} . . .')
        random_name = generate_string(generate_number())
        random_url_producto = generate_string(generate_number())
        random_url_img_producto = generate_string(generate_number())
        random_description = generate_string(generate_number())
        
        productos.append(Producto(
            codigo=j,#random()*10-1
            nombre_producto=random_name,
            url_producto=random_url_producto,
            url_img_producto=random_url_img_producto,
            precio=100.4
        ))

    Producto.objects.bulk_create(productos)
         
if __name__ == "__main__":
    print("Inicio de creación de productos")
    print("Por favor espere . . . ")
    start = time.strftime("%c")
    print(f'Fecha y hora de inicio: {start}')
    generate_producto(9) # cantidad de registros generados aleatoriamente
    end = time.strftime("%c")
    print(f'Fecha y hora de finalización: {end}')