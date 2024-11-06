# Generated by Django 5.1.3 on 2024-11-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies: list[str] = []

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('completed', models.BooleanField(default=False)),
                ('due_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('projects', models.ManyToManyField(to='project.project')),
            ],
        ),
    ]
