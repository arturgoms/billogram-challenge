# Generated by Django 4.0.4 on 2022-04-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("domain", "0005_discount_hide"),
    ]

    operations = [
        migrations.AddField(
            model_name="discount",
            name="enable",
            field=models.BooleanField(default=True, verbose_name="Enable"),
        ),
        migrations.AlterField(
            model_name="discount",
            name="hide",
            field=models.BooleanField(default=False, verbose_name="Hide"),
        ),
    ]
