# Generated by Django 4.1.2 on 2022-10-13 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carinfo', '0004_car_notes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Image',
        ),
    ]
