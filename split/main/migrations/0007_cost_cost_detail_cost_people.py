# Generated by Django 4.2.23 on 2025-07-16 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_costdetail_cost_remove_people_spent'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='cost_detail',
            field=models.ManyToManyField(to='main.costdetail'),
        ),
        migrations.AddField(
            model_name='cost',
            name='people',
            field=models.ManyToManyField(to='main.people'),
        ),
    ]
