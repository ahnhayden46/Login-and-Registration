from django.db import models
from django.contrib.auth.models import User


# The customer model
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    contact_number = models.CharField(max_length=11, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)


contact_choices = (('phone', 'PHONE'), ('email', 'EMAIL'),)
# The evaluation model


class Evaluation(models.Model):
    description = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.CASCADE)
    contact_method = models.CharField(
        max_length=6, choices=contact_choices, default='email')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.customer)
