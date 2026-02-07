from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Category
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name

# Supplier
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.supplier_name

# Medicine
class Medicine(models.Model):
    medicine_name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.medicine_name

# Batch
class Batch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=50)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.batch_number}"

# Warehouse
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    capacity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.warehouse_name

# Stock
class Stock(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.batch.medicine.medicine_name} - {self.quantity}"

# Purchase Order
class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Pending")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id}"

# Order Detail
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.medicine_name} ({self.quantity_ordered})"

# Transaction
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)
    reference_no = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.batch.medicine.medicine_name}"
