# Generated by Django 3.2.4 on 2021-06-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0007_alter_productos_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='media/imgproductos/'),
        ),
    ]
