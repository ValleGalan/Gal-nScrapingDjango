# Generated by Django 4.0.2 on 2022-06-25 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webscraping', '0003_alter_producto_idnombreproducto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='nombre_producto',
            field=models.CharField(max_length=1200, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='url_img_producto',
            field=models.CharField(max_length=1200, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='url_producto',
            field=models.CharField(max_length=1200, null=True),
        ),
    ]
