# Generated by Django 4.0.6 on 2023-01-10 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0018_prescription_presc_prescription_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='next_visit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='created_on',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]