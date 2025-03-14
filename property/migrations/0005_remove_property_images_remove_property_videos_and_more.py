# Generated by Django 5.1.6 on 2025-03-11 17:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_alter_property_property_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='images',
        ),
        migrations.RemoveField(
            model_name='property',
            name='videos',
        ),
        migrations.AlterField(
            model_name='property',
            name='amenities',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='property_images/')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='property.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='property_videos/')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='property.property')),
            ],
        ),
    ]
