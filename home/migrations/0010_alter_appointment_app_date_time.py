# Generated by Django 4.0.6 on 2023-01-08 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_remove_appointment_app_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='app_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]