from django.db import models
from django.conf import settings


# Create your models here.

class Category(models.Model):
    choice = models.CharField(max_length=100)

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name_plural = "Categories"


class Color(models.Model):
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.color


class Size(models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size


class Shop(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10000, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    shop = models.ForeignKey(Shop, related_name='shop', on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ManyToManyField(Size)
    color = models.ManyToManyField(Color)
    picture = models.ImageField(upload_to='picture', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    shop = models.ManyToManyField(Shop)

    def __str__(self):
        return F"{self.quantity} of {self.item.title} from {self.shop}"

    class Meta:
        ordering = ['-id']


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    cart = models.ManyToManyField(OrderItem)
    ref_code = models.CharField(max_length=30)
    update_code = models.CharField(max_length=4, blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=30)
    ordered = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    total = models.IntegerField(default=1)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, blank=True, null=True
    )
    packaged = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return F"{self.ref_code} to {self.location} "

    class Meta:
        ordering = ['-id']


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    billing_address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    tx_ref = models.CharField(max_length=1000)
    amount = models.FloatField()
    flw_ref = models.CharField(max_length=1000)
    tansaction_id = models.CharField(max_length=1000)
    status = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    ref_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.pk}"
