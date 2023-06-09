# Generated by Django 4.2.1 on 2023-06-02 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_product_preview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=250, verbose_name='Post Title')),
                ('slug', models.CharField(max_length=50, verbose_name='Slug')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Preview')),
                ('published_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('is_published', models.BooleanField(default=False, verbose_name='Published')),
                ('views', models.IntegerField(default=0, verbose_name='Views')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
        ),
    ]
