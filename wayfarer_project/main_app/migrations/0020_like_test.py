# Generated by Django 3.1.2 on 2020-11-06 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0019_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='test',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
