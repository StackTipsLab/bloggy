# Generated by Django 4.2.7 on 2023-12-22 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloggy', '0005_page_template_type_alter_post_post_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='template_type',
            field=models.CharField(blank=True, choices=[('newsletter', 'Newsletter'), ('naked', 'Naked'), ('default', 'Default')], default='default', help_text='Template type', max_length=20, null=True, verbose_name='Template type'),
        ),
    ]
