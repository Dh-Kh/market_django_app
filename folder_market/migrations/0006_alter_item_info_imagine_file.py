# Generated by Django 4.2 on 2023-05-06 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folder_market', '0005_alter_item_info_imagine_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_info',
            name='imagine_file',
            field=models.ImageField(null=True, upload_to='images/', verbose_name=''),
        ),
    ]
