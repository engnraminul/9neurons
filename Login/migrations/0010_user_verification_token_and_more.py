# Generated by Django 4.2.3 on 2023-07-29 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Login", "0009_alter_user_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="verification_token",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="verification_token_expiration",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
