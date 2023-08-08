# Generated by Django 4.2.3 on 2023-08-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Login", "0012_user_email_verify"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("Visitor", "Visitor"),
                    ("Member", "Member"),
                    ("Premium", "Premium"),
                ],
                default="Visitor",
                max_length=50,
            ),
        ),
    ]
