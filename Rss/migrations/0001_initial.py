# Generated by Django 5.0.6 on 2024-05-21 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Название источника', max_length=255, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, help_text='Описание источника', null=True, verbose_name='Описание')),
                ('url', models.URLField(help_text='Ссылка на источник', unique=True, verbose_name='Ссылка')),
                ('slug', models.SlugField(blank=True, editable=False, help_text='slug источника', max_length=255, null=True, unique=True, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания этой записи', verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now_add=True, help_text='Дата обновления этой записи', verbose_name='Обновлено')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='Ссылка на статью', verbose_name='Ссылка')),
                ('title', models.TextField(blank=True, help_text='Заголовок статьи', null=True, verbose_name='Заголовок')),
                ('summary_url', models.URLField(blank=True, help_text='Ссылка на пересказ статьи', null=True, verbose_name='Ссылка на пересказ')),
                ('summary', models.TextField(blank=True, help_text='Пересказ статьи', null=True, verbose_name='Пересказ')),
                ('image_url', models.URLField(blank=True, help_text='Ссылка на изображение статьи', null=True, verbose_name='Ссылка на изображение')),
                ('status', models.IntegerField(choices=[(0, 'DRAFT'), (1, 'PUBLISHED'), (2, 'DELETED'), (3, 'ERROR')], default=0, help_text='Статус статьи', verbose_name='Статус')),
                ('retry_count', models.IntegerField(default=0, help_text='Количество попыток обработки статьи', verbose_name='Количество попыток обработки статьи')),
                ('error_text', models.TextField(blank=True, help_text='Текст ошибки при обработке статьи', null=True, verbose_name='Текст ошибки')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания этой записи', verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now_add=True, help_text='Дата обновления этой записи', verbose_name='Обновлено')),
                ('source', models.ForeignKey(help_text='Источник статьи', on_delete=django.db.models.deletion.CASCADE, to='Rss.feed', verbose_name='Источник')),
            ],
            options={
                'unique_together': {('source', 'url')},
            },
        ),
    ]
