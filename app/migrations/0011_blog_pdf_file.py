# Generated by Django 4.2.1 on 2023-05-16 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_blog_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='pdf_file',
            field=models.FileField(blank=True, upload_to='pdf_files/', verbose_name='Файл(pdf)'),
        ),
    ]