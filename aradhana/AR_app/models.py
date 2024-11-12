from django.db import models

class SalesRecord(models.Model):
    date = models.CharField(max_length=50)
    amount = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    code = models.CharField(max_length=100)

    class Meta:
        db_table = 'sales_records'  # Use the existing table


class Inventory(models.Model):
    date = models.DateField()
    seller = models.CharField(max_length=255)
    seller_address = models.TextField()
    item_name = models.CharField(max_length=255)
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=100)

    class Meta:
        db_table = 'inventory'  # Use this name for the inventory table

class Data(models.Model):
    item_name = models.CharField(max_length=255)
    Wholesale_cost = models.DecimalField(max_digits=10, decimal_places=2)
    retail_cost = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=100)
    season = models.CharField(max_length=100)

    class Meta:
        db_table = 'Data'  # Use this name for the Data table

    def __str__(self):
        return f"{self.item_name} - {self.seller}"