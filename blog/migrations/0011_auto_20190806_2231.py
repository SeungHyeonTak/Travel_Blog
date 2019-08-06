# Generated by Django 2.2.2 on 2019-08-06 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20190806_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='city',
            field=models.CharField(default='', help_text='도시를 입력하세요', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='about',
            name='country',
            field=models.CharField(default='', help_text='국가를 입력하세요', max_length=50),
            preserve_default=False,
        ),
    ]
