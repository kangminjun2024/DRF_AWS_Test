from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = (    #앞에꺼가 DB저장되는거 뒤에꺼가 사용자에게 보여주는거
        ("F", "Fruit"),
        ("V", "Vegetable"),
        ("M", "Meat"),
        ("O", "Other"),
    )
    
    name = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.name
    