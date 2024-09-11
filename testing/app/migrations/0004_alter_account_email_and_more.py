# Generated by Django 5.0.7 on 2024-09-03 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_account_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='fixeddeposit',
            name='account_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.account'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='tenure',
            field=models.PositiveIntegerField(),
        ),
    ]
