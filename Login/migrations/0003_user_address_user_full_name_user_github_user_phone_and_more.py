# Generated by Django 4.2.3 on 2023-07-24 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Login", "0002_rename_first_address_profile_address_profile_github"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="full_name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="github",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
        ),
        migrations.AddField(
            model_name="user",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approve", "Approved"),
                    ("disapprove", "Disapproved"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="university_name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]
