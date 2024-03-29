# Generated by Django 3.0.4 on 2020-05-05 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb', models.IntegerField()),
                ('name', models.CharField(max_length=32)),
                ('birth', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb', models.IntegerField()),
                ('title', models.CharField(max_length=32)),
                ('year', models.IntegerField()),
                ('actors', models.ManyToManyField(to='brain.Actor')),
            ],
        ),
    ]
