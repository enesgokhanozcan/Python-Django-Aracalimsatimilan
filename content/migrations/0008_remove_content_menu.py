# Generated by Django 3.1.7 on 2021-05-27 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_content_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='menu',
        ),
    ]
