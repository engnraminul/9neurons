# Generated by Django 4.2.3 on 2023-08-15 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Models", "0005_model_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="parent_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Models.category",
            ),
        ),
    ]
