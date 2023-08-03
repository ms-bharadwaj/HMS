# Generated by Django 4.0.6 on 2023-01-08 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_appointment_app_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='app_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctorId',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctorName',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='symptoms',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]