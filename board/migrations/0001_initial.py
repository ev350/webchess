# Generated by Django 2.0.5 on 2018-05-06 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fen', models.CharField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', max_length=256)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('date_ended', models.DateTimeField(null=True)),
                ('is_won', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_position', models.CharField(max_length=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='board.Board')),
            ],
        ),
    ]