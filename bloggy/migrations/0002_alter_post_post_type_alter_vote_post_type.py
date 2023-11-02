# Generated by Django 4.2.6 on 2023-11-01 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloggy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(blank=True, choices=[['article', 'Article'], ['lesson', 'Lesson']], default='article', help_text='Post type', max_length=20, null=True, verbose_name='Post type'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='post_type',
            field=models.CharField(choices=[['article', 'Article'], ['lesson', 'Lesson']], help_text='Select content type', max_length=20, verbose_name='Content type'),
        ),
    ]
