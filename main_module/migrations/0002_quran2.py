# Generated by Django 2.1.3 on 2018-12-22 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quran2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ChapterNArabic', models.CharField(max_length=9999)),
            ],
        ),
    ]
