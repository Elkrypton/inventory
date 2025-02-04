# Generated by Django 4.2.15 on 2025-02-02 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coach_number', models.CharField(max_length=20)),
                ('departure_location', models.CharField(max_length=100)),
                ('arrival_location', models.CharField(max_length=100)),
                ('seat_capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('feedback', models.TextField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='SearchProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=50)),
                ('product_img', models.ImageField(upload_to='images/')),
                ('quantity', models.IntegerField()),
                ('date_of_production', models.DateTimeField()),
                ('sku', models.CharField(max_length=50, unique=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
