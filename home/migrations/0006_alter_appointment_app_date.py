# Generated by Django 4.0.6 on 2023-01-08 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_doctor_available_doctor_department_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='app_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]