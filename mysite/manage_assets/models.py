from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    people = models.IntegerField()
    address = models.CharField(max_length=40)
    city = models.CharField(max_length=10)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Person(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=20)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=20)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='residents')
    email = models.CharField(max_length=30)


class Category(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    type = models.CharField(max_length=10)
    quantity = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Manufacturer(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    assets = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Supplier(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    contact_name = models.CharField(max_length=20)
    url = models.CharField(max_length=20)
    assets = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Asset(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    assetname = models.CharField(max_length=30)
    serial = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='assets')
    employeeid = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, related_name='assets')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, related_name='related_assets')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='related_assets')
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)

