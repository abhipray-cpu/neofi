# Generated by Django 5.0.2 on 2024-02-20 16:51

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='Create your note', verbose_name='note_content')),
                ('share', models.TextField(default='[]', verbose_name='shared_users')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='note_owner')),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev', models.TextField(verbose_name='old_content')),
                ('new', models.TextField(verbose_name='new_content')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user', verbose_name='changed_by')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_notes.note', verbose_name='note_id')),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
