# Generated by Django 4.2.19 on 2025-02-19 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitepages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drink',
            name='category',
            field=models.CharField(choices=[('coffee', 'Coffee'), ('tea', 'Tea'), ('other', 'Other')], max_length=10),
        ),
    ]
