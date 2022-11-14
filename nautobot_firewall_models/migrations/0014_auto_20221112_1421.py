# Generated by Django 3.2.15 on 2022-11-12 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nautobot_firewall_models', '0013_auto_20221112_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationobject',
            name='category',
            field=models.CharField(blank=True, max_length=48),
        ),
        migrations.AlterField(
            model_name='applicationobject',
            name='default_ip_protocol',
            field=models.CharField(blank=True, max_length=48),
        ),
        migrations.AlterField(
            model_name='applicationobject',
            name='default_type',
            field=models.CharField(blank=True, max_length=48),
        ),
        migrations.AlterField(
            model_name='applicationobject',
            name='risk',
            field=models.PositiveIntegerField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='applicationobject',
            name='subcategory',
            field=models.CharField(blank=True, max_length=48),
        ),
        migrations.AlterField(
            model_name='applicationobject',
            name='technology',
            field=models.CharField(blank=True, max_length=48),
        ),
    ]
