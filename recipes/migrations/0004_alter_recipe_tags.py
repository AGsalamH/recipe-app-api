# Generated by Django 5.0.4 on 2024-05-20 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_tags'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='tags.tag'),
        ),
    ]
