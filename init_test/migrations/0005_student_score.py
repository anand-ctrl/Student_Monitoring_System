# Generated by Django 3.1.7 on 2021-03-20 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('init_test', '0004_auto_20210319_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='student_score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organised', models.BooleanField(default=False)),
                ('stubborn', models.BooleanField(default=False)),
                ('introvert', models.BooleanField(default=False)),
                ('extrovert', models.BooleanField(default=False)),
                ('agreeable', models.BooleanField(default=False)),
                ('passive', models.BooleanField(default=False)),
                ('creative', models.BooleanField(default=False)),
                ('unpredictable', models.BooleanField(default=False)),
                ('neurotic', models.BooleanField(default=False)),
                ('regularity', models.BooleanField(default=False)),
                ('efficiency', models.BooleanField(default=False)),
                ('teamwork', models.BooleanField(default=False)),
                ('memory', models.BooleanField(default=False)),
                ('psa', models.BooleanField(default=False)),
                ('business', models.BooleanField(default=False)),
                ('management', models.BooleanField(default=False)),
                ('Technical', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
