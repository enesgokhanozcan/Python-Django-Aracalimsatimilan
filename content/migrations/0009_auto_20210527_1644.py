# Generated by Django 3.1.7 on 2021-05-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_remove_content_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='status',
            field=models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], max_length=10),
        ),
    ]
