# Generated by Django 5.0.2 on 2024-03-16 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_soft', '0004_alter_product_options_alter_purchase_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saledetail',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='saledetail',
            name='created_user',
        ),
        migrations.RemoveField(
            model_name='saledetail',
            name='modifier_user',
        ),
        migrations.RemoveField(
            model_name='saledetail',
            name='updated_at',
        ),
    ]
