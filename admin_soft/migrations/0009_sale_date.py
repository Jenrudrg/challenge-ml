# Generated by Django 5.0.2 on 2024-03-17 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_soft', '0008_purchase_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
