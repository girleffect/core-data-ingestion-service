# Generated by Django 2.1.1 on 2019-01-16 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_ingestion_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storedfiles',
            name='category',
            field=models.CharField(blank=True, choices=[('offline_survey_data', 'Offline Survey Data')], max_length=255, null=True),
        ),
    ]
