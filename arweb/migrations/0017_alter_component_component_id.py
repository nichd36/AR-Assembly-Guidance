# Generated by Django 4.2.9 on 2024-03-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arweb', '0016_component_picture_alter_component_component_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='component_id',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
