# Generated by Django 5.0.6 on 2024-08-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rss', '0002_feed_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='related',
            field=models.ManyToManyField(blank=True, help_text='Похожие записи', to='Rss.article', verbose_name='Похожие записи'),
        ),
    ]