# Generated by Django 2.0.1 on 2019-03-13 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(max_length=120)),
                ('products', models.ManyToManyField(blank=True, related_name='tags', to='prods.Product')),
            ],
        ),
    ]
