from django.db import models
# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    desc = models.TextField(max_length=1000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")


    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone = models.CharField(max_length=100)
    Desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.Name

# creating model for checkout
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name +' and order_Id : ' +  str(self.order_id)

# creating order update model
class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default='')
    update_desc = models.CharField(max_length=1000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
            return 'order_id : '+ str(self.order_id)

class ProductView(models.Model):
    productId = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)

    def __str__(self):
            return 'product_id Review : '+ str(self.profuctId)
# update_desc[0:16] + '...'            