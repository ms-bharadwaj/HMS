# Generated by Django 4.0.6 on 2023-01-21 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_invoice_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='astatus',
            new_name='istatus',
        ),
    ]
