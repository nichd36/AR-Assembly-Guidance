# Generated by Django 4.2.9 on 2024-01-28 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arweb.product')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arweb.step')),
            ],
        ),
    ]
