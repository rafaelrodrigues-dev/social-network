# Generated by Django 5.1.5 on 2025-04-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0007_alter_comment_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='text',
            field=models.TextField(max_length=500, verbose_name='Text'),
        ),
    ]
