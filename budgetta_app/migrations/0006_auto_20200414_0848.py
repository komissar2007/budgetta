# Generated by Django 3.0.5 on 2020-04-14 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgetta_app', '0005_auto_20200414_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetta_app.Category'),
        ),
    ]
