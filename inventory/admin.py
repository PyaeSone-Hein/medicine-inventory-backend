from django.contrib import admin

# Register your models here.
from .models import (
    Category,
    Supplier,
    Medicine,
    Batch,
    Warehouse,
    Stock,
    Order,
    OrderDetail,
    Transaction
)

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Medicine)
admin.site.register(Batch)
admin.site.register(Warehouse)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Transaction)
