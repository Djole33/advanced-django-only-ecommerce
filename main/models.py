from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/products/", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, default="", blank=True, null=True)
    image = models.ImageField(upload_to="images/products/")
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name

class Review(models.Model):
    class Star(models.IntegerChoices):
        UNUSABLE = 1
        BAD = 2
        OK = 3
        GOOD = 4
        EXCELLENT = 5

    user = models.ForeignKey(User, related_name='user_review', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_review', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=Star)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=2000)

    def __str__(self):
        return f'{self.title}'