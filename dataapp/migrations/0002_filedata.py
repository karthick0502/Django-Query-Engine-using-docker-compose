    # Generated by Django 4.2.13 on 2024-06-26 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('uploaded_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_data', to='dataapp.uploadedfile')),
            ],
        ),
    ]