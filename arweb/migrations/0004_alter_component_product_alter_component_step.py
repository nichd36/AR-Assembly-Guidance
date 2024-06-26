# Generated by Django 4.2.9 on 2024-01-28 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arweb', '0003_alter_product_desc_alter_step_instruction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='arweb.product'),
        ),
        migrations.AlterField(
            model_name='component',
            name='step',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='arweb.step'),
        ),
    ]
