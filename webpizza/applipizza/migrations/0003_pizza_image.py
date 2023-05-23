# Generated by Django 2.2.28 on 2023-05-15 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applipizza', '0002_composition'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='image',
            field=models.ImageField(default='static/applipizza/img/pizza_cover.png', upload_to='static/applipizza/img/', verbose_name="L'image de la pizza"),
            preserve_default=False,
        ),
    ]
