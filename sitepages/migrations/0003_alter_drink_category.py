# Generated by Django 4.2.19 on 2025-02-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitepages', '0002_alter_drink_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drink',
            name='category',
            field=models.CharField(choices=[('coffee', 'Coffee'), ('tea', 'Tea'), ('hot chocolate', 'Hot Chocolate'), ('other', 'Other')], max_length=15),
        ),
    ]
