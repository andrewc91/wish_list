from __future__ import unicode_literals
from django.db import models
from ..login_app.models import Person
from datetime import datetime

# Create your models here.
class ProductManager(models.Manager):
    #validations to add products
    def addProduct(self, input, user):
        errors = []

        if len(input['item']) == 0:
            errors.append('Please fill out entry')

        if len(input['item']) < 4:
            errors.append('Entry must be more than 3 characters')

        # if there's no errors
        if len(errors) == 0:
            date = datetime.now()
            product = Product.objects.create(item=input['item'], user=user, date_added=date)
            product.group.add(user)
            product.save()
            return (True, 'Successfully added product to your wish list!')
        else:
            return (False, errors)

    # join the products!
    def joinProduct(self, item_id, user):
        item = Product.objects.get(id=item_id)
        item.group.add(user)
        item.save()
        return (True, "Successfully added item to Wishlist!")

class Product(models.Model):
    item = models.CharField(max_length=255)
    date_added = models.DateField()
    user = models.ForeignKey(Person)
    group = models.ManyToManyField(Person, related_name="wishlist")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()
