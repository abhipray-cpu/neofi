# Generated by Django 5.0.2 on 2024-02-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='note',
            field=models.IntegerField(verbose_name='note_id'),
        ),
        migrations.AlterField(
            model_name='change',
            name='user',
            field=models.IntegerField(null=True, verbose_name='changed_by'),
        ),
    ]