# Generated by Django 4.1.2 on 2023-02-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='header_text',
            field=models.CharField(blank=True, max_length=3000),
        ),
    ]
