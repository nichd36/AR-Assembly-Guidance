# Generated by Django 4.2.9 on 2024-02-07 01:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('arweb', '0011_component_component_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='component',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]