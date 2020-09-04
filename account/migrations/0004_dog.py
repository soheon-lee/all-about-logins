# Generated by Django 3.0.8 on 2020-09-02 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200713_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('jong', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
            ],
            options={
                'db_table': 'dogs',
            },
        ),
    ]
