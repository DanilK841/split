from django.db import models
from django.db.models import ForeignKey

class Cost(models.Model):
    name = models.CharField(max_length=50)
    # people = models.ManyToManyField(People, related_name='cost')
    # cost_detail = models.ManyToManyField(CostDetail, related_name='cost')

class People(models.Model):

    name = models.CharField(max_length=30)
    telegram = models.CharField(max_length=70)
    cost = models.ForeignKey(Cost, on_delete=models.CASCADE, related_name='peoples')
    def __str__(self):
        return self.name



class CostDetail(models.Model):
    name = models.CharField(max_length=150, null=False)
    people_cost = models.ForeignKey(People, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    people_share = models.ManyToManyField(People, related_name='people_share', )
    cost = models.ForeignKey(Cost, on_delete=models.CASCADE, related_name='costdetail')
    # cost = models.ManyToManyField(Cost)


# todo добавить ссылку url






# todo добавить выбор валюты и конвертацию к одной валюте


