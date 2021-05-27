# Generated by Django 3.1.7 on 2021-05-27 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20210527_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='category',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='image',
        ),
        migrations.AddField(
            model_name='content',
            name='menu',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.menu'),
        ),
        migrations.AddField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('menu', 'menu'), ('duyuru', 'duyuru'), ('ilan', 'ilan')], default=2, max_length=10),
            preserve_default=False,
        ),
    ]