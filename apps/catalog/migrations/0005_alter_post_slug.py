# Generated by Django 4.2.1 on 2023-06-03 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Slug'),
        ),
    ]
