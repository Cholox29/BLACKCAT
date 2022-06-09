
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tienda', '0015_auto_20210705_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='items',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.productos'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.order'),
        ),
        migrations.DeleteModel(
            name='Clientes',
        ),
    ]
