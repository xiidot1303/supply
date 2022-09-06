from django.db import models

class Applicant(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='')
    username = models.CharField(null=True, blank=True, max_length=256)
    firstname = models.CharField(null=True, blank=True, max_length=256)
    phone = models.CharField(null=True, blank=True, max_length=16, default='')
    lang = models.CharField(null=True, blank=True, max_length=4)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()

class Supplier(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='')
    username = models.CharField(null=True, blank=True, max_length=256)
    firstname = models.CharField(null=True, blank=True, max_length=256)
    phone = models.CharField(null=True, blank=True, max_length=16, default='')
    lang = models.CharField(null=True, blank=True, max_length=4)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True)
    access = models.BooleanField(null=True, blank=True, default=False)
    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()

class Order(models.Model):
    product = models.CharField(null=True, blank=True, max_length=255)
    type = models.CharField(null=True, blank=True, max_length=255)
    amount = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True, max_length=1024)
    product_obj = models.ForeignKey('Product', null=True, blank=True, on_delete=models.PROTECT)


class Statement(models.Model):
    user = models.ForeignKey(
        'app.Applicant', null=True, blank=True, on_delete=models.PROTECT
    )
    date = models.DateTimeField(null=True, blank=True, max_length=64)
    orders = models.ManyToManyField('app.Order', blank=True)
    status = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        choices=(
            ("wait", "waiting"),
            ("end", "end"),
            ("cancel", "cancelled"),
        ),
    )
    supplier = models.ForeignKey('Supplier', null=True, blank=True, on_delete=models.PROTECT)

class Supply(models.Model): # offers of Suppliers
    supplier = models.ForeignKey('Supplier', null=True, blank=True, on_delete=models.PROTECT)
    statement = models.ForeignKey('Statement', null=True, blank=True, on_delete=models.PROTECT)
    price = models.CharField(null=True, blank=True, max_length=64)
    due = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        choices=(
            ("wait", "waiting"),
            ("conf", "confirmed"),
            ("cancel", "cancelled")
        ),
    )

class Product(models.Model):
    keyid = models.CharField(null=True, blank=True, max_length=255)
    product_id = models.CharField(null=True, blank=True, max_length=255)
    title = models.CharField(null=True, blank=True, max_length=10000)
    amount = models.IntegerField(null=True, blank=True)
    warehouse = models.CharField(null=True, blank=True, max_length=255)
    warehouse_id = models.CharField(null=True, blank=True, max_length=64)
    type_id = models.CharField(null=True, blank=True, max_length=64)
    type = models.CharField(null=True, blank=True, max_length=255)


    def __str__(self) -> str:
        return self.title or super().__str__()



class Notification(models.Model):
    group_id = models.CharField(null=True, blank=True, max_length=16)
    title = models.CharField(null=True, blank=True, max_length=255)
    type = models.CharField(
        null=True, 
        blank=True, 
        max_length=16, 
        choices=(
            ('order', 'order'),
            ('supply', 'supply'),

        )
        )
    access = models.BooleanField(null=True, blank=True, default=False)