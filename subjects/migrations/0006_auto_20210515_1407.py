# Generated by Django 3.1.7 on 2021-05-15 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0005_auto_20210322_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggested_subject',
            name='suggested_subjects',
            field=models.JSONField(),
        ),
    ]
