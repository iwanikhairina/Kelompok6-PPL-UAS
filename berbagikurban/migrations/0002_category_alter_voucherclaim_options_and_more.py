# Generated by Django 5.2.2 on 2025-06-10 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berbagikurban', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nama Kategori')),
                ('description', models.TextField(blank=True, verbose_name='Deskripsi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategori',
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='voucherclaim',
            options={'ordering': ['-claimed_at'], 'verbose_name': 'Klaim Voucher', 'verbose_name_plural': 'Klaim Vouchers'},
        ),
        migrations.AddField(
            model_name='voucherclaim',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='Dikonfirmasi'),
        ),
        migrations.AddField(
            model_name='voucherclaim',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Catatan'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='berbagikurban.category', verbose_name='Kategori'),
        ),
    ]
