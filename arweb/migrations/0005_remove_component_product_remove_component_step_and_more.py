# Generated by Django 4.2.9 on 2024-01-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arweb', '0004_alter_component_product_alter_component_step'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='product',
        ),
        migrations.RemoveField(
            model_name='component',
            name='step',
        ),
        migrations.AddField(
            model_name='product',
            name='components',
            field=models.ManyToManyField(blank=True, to='arweb.component'),
        ),
    ]
