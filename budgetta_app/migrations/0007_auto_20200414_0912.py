# Generated by Django 3.0.5 on 2020-04-14 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetta_app', '0006_auto_20200414_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(max_length=100),
        ),
    ]
