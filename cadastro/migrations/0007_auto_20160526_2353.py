# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-26 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0006_produto_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='tipo',
            field=models.CharField(choices=[('novo', 'Novo'), ('usado', 'Usado')], default='novo', max_length=1),
        ),
    ]
