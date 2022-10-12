from django.db import models
from user.models import User

# Create your models here.

# class Order(models.Model):

#     RECEIVED = "R"
#     PROCESSING = "P"
#     COMPLETED = "C"
#     DELIVERED = "D"
#     CANCELLED = "Cancelled"
#     ORDER_STATUS_CHOICES = (
#         (RECEIVED, "Order Received"),
#         (PROCESSING, "Processing"),
#         (COMPLETED, "Completed"),
#         (DELIVERED, "Delivered"),
#         (CANCELLED, "Cancelled"),
#     )

#     NOT_PAID = "NP"
#     PART_PAYMENT = "PP"
#     FULL_PAYMENT = "FP"
#     PAYMENT_STATUS_CHOICES = (
#         (NOT_PAID, "Unpaid"),
#         (PART_PAYMENT, "Part"),
#         (FULL_PAYMENT, "Processing"),
#     )
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     client = models.ForeignKey(User, on_delete=models.CASCADE)
#     total_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_status = models.CharField(
#         max_length=100, choices=PAYMENT_STATUS_CHOICES, default=NOT_PAID
#     )
#     order_status = models.CharField(
#         max_length=50, choices=ORDER_STATUS_CHOICES, default=RECEIVED
#     )
#     ordered_on = models.DateTimeField(auto_now_add=True)

# class Item(models.Model):
    
#     name = models.CharField(max_length=50)
#     image = models.ImageField()
#     ordered = models.BooleanField(default=False)
#     date_uploaded = models.DateTimeField(auto_now_add=True)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)

# class OrderedItem(models.Model):

#     FROM_ME = "FM"
#     FROM_STORE = "FS"
#     FABRIC_SOURCE_OPTIONS = ((FROM_STORE, "Store"), (FROM_ME, "Personal"))

#     order = models.ManyToManyField(Order)
#     fabric_source = models.CharField(max_length=10, choices=FABRIC_SOURCE_OPTIONS, default=FROM_ME)
#     quantity = models.IntegerField(default=1)
#     unit_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     total_item_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)


# class OrderPayment(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
#     paid_on = models.DateTimeField(auto_now_add=True)
