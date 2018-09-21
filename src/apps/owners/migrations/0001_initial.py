# Generated by Django 2.1.1 on 2018-09-21 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(blank=True, default='', max_length=100)),
                ('amount', models.DecimalField(decimal_places=3, max_digits=8)),
            ],
        ),
    ]