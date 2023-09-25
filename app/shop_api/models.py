from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    class Status(models.TextChoices):
        OPEN = "OP", "Open"
        CLOSED = "CL", "Closed"

    address = models.CharField(max_length=120, blank=False, null=False)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.CLOSED)


class RestaurantMenuItem(models.Model):
    restaurant_id = models.ForeignKey(Restaurant,
                                      on_delete=models.CASCADE,
                                      related_name="menu_items")
    name = models.CharField(max_length=60, blank=False, null=False)
    price = models.FloatField()
    image = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()


class Customer(models.Model):
    phone = PhoneNumberField(blank=False)
    email = models.EmailField(max_length=254, blank=True)
    address = models.CharField(max_length=120, blank=False, null=False)


class Courier(models.Model):
    class Status(models.TextChoices):
        FREE = "FT", "Waiting for a task"
        WAIT = "WG", "Waiting for goods"
        DELIVER = "DL", "Delivery OK"
        OFF = "OF", "Does not work"
        PROBLEM = "DP", "Delivery delay"


    phone = PhoneNumberField(blank=False)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.OFF)
    coordinates = models.CharField(blank=True, null=True)


class Order(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 1
        REFUSED = 2
        PAYMENT = 3
        PAID = 4
        REJECT = 5
        ACCEPT = 6
        CANCELED = 7
        COOKING = 8
        READY = 9
        DELIVER = 10
        DELIVERED = 11


    customer_id = models.ForeignKey(Customer,
                                    on_delete=models.DO_NOTHING,
                                    related_name='orders')
    restaurant_id = models.ForeignKey(Restaurant,
                                      on_delete=models.DO_NOTHING,
                                      related_name='orders')
    status = models.IntegerField(choices=Status.choices,
                                 default=Status.CREATED)
    courier_id = models.ForeignKey(Courier,
                                   on_delete=models.DO_NOTHING,
                                   blank=True,
                                   null=True,
                                   default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivering_started = models.DateTimeField(blank=True,
                                              null=True,
                                              default=None)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    restaurant_menu_item = models.ForeignKey(RestaurantMenuItem,
                                             on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()