from django.db import models
from django.contrib.auth.models import User
import datetime


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
	name = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True)

	


class Product(models.Model):
	name = models.CharField(max_length=200,null=True)
	description = models.CharField(max_length=1000,null=True)
	price = models.IntegerField()
	digital = models.BooleanField(default=False, null=True, blank=False)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url= self.image.url
		except:
			url= "" 
		return url


class OrderInfo(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)
    delievered=models.BooleanField(default=False, null=True, blank=False)

    def __int__(self):
    	return self.order_id

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete= models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=100, null=True)


	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([ item.get_total for item in orderitems ]) 
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([ item.quantity for item in orderitems ]) 
		return total


	

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
	 	total = self.product.price * self.quantity
	 	return total




class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,blank=True)
	address=models.CharField(max_length=200, null=False)
	city=models.CharField(max_length=200,null=False)
	state=models.CharField(max_length=200,null=False)
	zipcode=models.CharField(max_length=200,null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


class Comment(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	subject = models.CharField(max_length=200, null=True)
	comment = models.CharField(max_length=200, null=True)
	rate = models.IntegerField(default=1)
	create_at = models.DateTimeField(auto_now_add=True)
	ctype=models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.comment

  