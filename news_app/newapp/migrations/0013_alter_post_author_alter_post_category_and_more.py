# Generated by Django 4.0.1 on 2022-02-13 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0012_alter_post_author_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default='John', on_delete=django.db.models.deletion.CASCADE, to='newapp.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default='Nature', null=True, on_delete=django.db.models.deletion.CASCADE, to='newapp.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='dateCreation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
