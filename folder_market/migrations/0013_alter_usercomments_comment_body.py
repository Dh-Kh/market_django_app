# Generated by Django 4.2 on 2023-05-07 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folder_market', '0012_alter_usercomments_comment_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercomments',
            name='comment_body',
            field=models.CharField(max_length=700),
        ),
    ]
