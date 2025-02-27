# Generated by Django 4.2.19 on 2025-02-19 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(choices=[('coffee', 'Coffee'), ('tea', 'Tea')], max_length=10)),
                ('ingredients', models.TextField(help_text='List ingredients separated by commas')),
                ('method', models.TextField(help_text='Preparation method')),
            ],
        ),
    ]
