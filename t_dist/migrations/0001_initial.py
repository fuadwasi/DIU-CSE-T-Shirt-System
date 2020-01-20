# Generated by Django 3.0.2 on 2020-01-20 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sID', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('givenby', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='not_taken', max_length=100)),
            ],
        ),
    ]
