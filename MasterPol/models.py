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

    def __str__(self):
        return f"{self.name} (Коэффицент: {self.product_type_ratio})"

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

    def get_discount(self):
        total_quantity = Partner_product.objects.filter(
            partner=self
        ).aggregate(total=models.Sum('product_quantity'))['total'] or 0

        if total_quantity >= 300000:
            return 15
        elif total_quantity >= 50000:
            return 10
        elif total_quantity >= 10000:
            return 5
        else:
            return 0

class Partner_product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    date = models.DateField()

class Material_type(models.Model):
    type = models.CharField(max_length=100)
    material_scrap_percentage = models.FloatField()

    def __str__(self):
        return f"{self.type} (брак: {self.material_scrap_percentage}%)"