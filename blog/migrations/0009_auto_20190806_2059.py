# Generated by Django 2.2.2 on 2019-08-06 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20190806_2051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='message',
            new_name='text',
        ),
    ]