from django.db import models

# CLASES  con el ORM se convertira en una tabla 
class NombreProducto(models.Model):
    idnombreproducto = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=500, default='DEFAULT VALUE')  
    def __str__(self):
        return self.idnombreproducto

class Producto(models.Model):
    idnombreproducto = models.ForeignKey('NombreProducto', on_delete=models.CASCADE,null=True,related_name='webscraping' ) 
    idproducto = models.AutoField(primary_key=True)
    nombre_producto= models.CharField(max_length=1200 ,null=True )
    precio =models.IntegerField(null=True)                                                              #DecimalField(max_digits=20,decimal_places=2,null=True )# 
    url_producto=models.CharField(max_length=1200 ,null=True )
    url_img_producto=models.CharField(max_length=1200 ,null=True )  

    def __str__(self):
        texto="{0} {1}"
        return texto.format((self.idnombreproducto,self.idproducto))  
        #para mostrar mi informacion en admin saldria el nombre+precio
    
     
 



