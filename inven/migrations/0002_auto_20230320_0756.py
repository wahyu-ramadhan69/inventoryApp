# Generated by Django 2.2.19 on 2023-03-20 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inven', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barang',
            name='penguasaan',
        ),
        migrations.RemoveField(
            model_name='barang',
            name='tahun_perolehan',
        ),
    ]