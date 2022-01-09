# Generated by Django 3.1.2 on 2022-01-09 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thjcrm', '0003_auto_20220109_0259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='activity',
        ),
        migrations.AddField(
            model_name='survey',
            name='activity',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to='thjcrm.activity'),
            preserve_default=False,
        ),
    ]