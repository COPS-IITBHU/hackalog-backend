# Generated by Django 3.1.2 on 2020-10-12 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20201011_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='handle',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='interests',
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='uid',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
