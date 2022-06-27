from django.contrib import admin
#importo el modelo Producto que cree
from .models import Producto ,NombreProducto
#importar cvs
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

# REGISTRO LOS MODELOS PARA ADMINISTRARLOS CON EL ADMINISTRADOR DJANGO
admin.site.register(Producto)
admin.site.register(NombreProducto)
# CVS

class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
class ProductoAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
    search_fields = ['nombre_producto']
    resources_class = ProductoResource
