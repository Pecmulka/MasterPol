from django.db import models

class Region (models.Model):
    name = models.CharField(max_length=100)

class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class Street (models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

class Address (models.Model):
    postal_code = models.BigIntegerField(primary_key=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    house_number = models.IntegerField()

class Product_type(models.Model):
    name = models.CharField(max_length=100)
    product_type_ratio = models.FloatField()

class Product (models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Product_type, on_delete=models.CASCADE)
    partner_min_price = models.FloatField()

class Partner_type(models.Model):
    name = models.CharField(max_length=100)

class Partner(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Partner_type, on_delete=models.CASCADE)
    CEO = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    INN = models.CharField(max_length=100)
    rating = models.IntegerField()
    discount = models.IntegerField(default=0)

class Partner_product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    date = models.DateField()

    def total_amount(self):
        """Метод для подсчета общей суммы покупки"""
        return self.product_quantity * self.product.partner_min_price * (1 - (self.partner.discount / 100))
