# Generated by Django 3.0.5 on 2020-04-14 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetta_app', '0004_auto_20200414_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
