# Generated by Django 5.0.4 on 2024-04-24 07:51

import przegladarkaobrazkow.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('przegladarkaobrazkow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='svgimage',
            name='image',
            field=models.TextField(blank=True, default=przegladarkaobrazkow.models.default_svg_content),
        ),
    ]
