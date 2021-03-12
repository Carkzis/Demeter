# Generated by Django 3.1.7 on 2021-03-11 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('country', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('continent', models.CharField(max_length=20)),
                ('national_dish', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.CharField(max_length=20)),
                ('meal', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demeter_app.countries')),
            ],
        ),
    ]
