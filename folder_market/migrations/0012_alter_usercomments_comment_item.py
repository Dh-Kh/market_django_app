# Generated by Django 4.2 on 2023-05-07 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('folder_market', '0011_usercomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercomments',
            name='comment_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='folder_market.item_info'),
        ),
    ]
