# Generated by Django 2.0.8 on 2018-08-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='alternative_text',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]