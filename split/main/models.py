from django.db import models
from django.db.models import ForeignKey


class Cost(models.Model):
    name = models.CharField(max_length=50)
# todo добавить ссылку url

class People(models.Model):
    name = models.CharField(max_length=30)
    telegram = models.CharField(max_length=70)
    spent = models.ForeignKey(Cost, on_delete=models.CASCADE)

class CostDetail(models.Model):
    people_cost = models.ForeignKey(People, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    people_share = models.ManyToManyField(People, related_name='people_share')
# todo добавить выбор валюты и конвертацию к одной валюте

