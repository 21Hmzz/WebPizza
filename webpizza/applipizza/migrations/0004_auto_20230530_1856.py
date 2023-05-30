# Generated by Django 3.2.18 on 2023-05-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applipizza', '0003_pizza_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='promotions',
            field=models.BooleanField(default=0, verbose_name='La pizza est-elle en promotion ?'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name="L'image de la pizza"),
        ),
    ]
