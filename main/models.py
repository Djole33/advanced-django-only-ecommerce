from django.db import models

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
