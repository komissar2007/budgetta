# Generated by Django 3.0.5 on 2020-04-14 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetta_app', '0002_auto_20200414_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(max_length=200),
        ),
    ]
