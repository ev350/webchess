# Generated by Django 2.0.5 on 2018-05-13 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='host_color',
            field=models.CharField(choices=[(1, 'w'), (2, 'b')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]
