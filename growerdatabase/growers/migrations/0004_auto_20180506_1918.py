# Generated by Django 2.0.5 on 2018-05-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growers', '0003_smsqueue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idgenerator',
            name='id_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='smsqueue',
            name='cellphone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='smsqueue',
            name='message',
            field=models.CharField(max_length=15),
        ),
    ]