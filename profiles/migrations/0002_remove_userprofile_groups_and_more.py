# Generated by Django 5.1.3 on 2024-11-29 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="is_superuser",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="user_permissions",
        ),
    ]
