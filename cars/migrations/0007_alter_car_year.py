# Generated by Django 5.1.4 on 2025-01-08 19:57

import cars.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_alter_car_options_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1960), cars.models.max_value_current_year], verbose_name='Год выпуска'),
        ),
    ]
