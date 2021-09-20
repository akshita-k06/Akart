from django.db import models
from datetime import datetime

class product(models.Model):
    id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    product_description=models.CharField(max_length=500)
    product_pubdate=models.DateField()
    catagory=models.CharField(max_length=50,default="")
    subcatagory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to="akart/images",default="")

    def __str__(self):
        return self.product_name

class contactdetails(models.Model):
    contact_id=models.AutoField(primary_key=True)
    contact_name=models.CharField(max_length=70)
    contact_email=models.CharField(max_length=50)
    contact_phone=models.BigIntegerField() 
    contact_feedback=models.CharField(max_length=500)

    def __str__(self):
        return self.contact_name

class orderdetails(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json= models.TextField()
    orderamount=models.IntegerField(default=0)
    ordername=models.CharField(max_length=90)
    orderaddress=models.CharField(max_length=150)
    orderaddress1=models.CharField(max_length=150)
    ordercontact=models.BigIntegerField() 
    ordercontact1=models.BigIntegerField() 
    ordercity=models.CharField(max_length=40)
    orderstate=models.CharField(max_length=40)
    orderpincode=models.BigIntegerField() 
    orderemail=models.CharField(max_length=70)
    orderpassword=models.CharField(max_length=50)
    
    def __str__(self):
        return self.ordername

class ordertracker(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(orderdetails,on_delete=models.CASCADE,default=None)
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7]+"...."

class OrderPayment(models.Model):
    id=models.AutoField(primary_key=True)
    order_id= models.ForeignKey(orderdetails,on_delete=models.CASCADE,default=None)
    TXNID = models.CharField(max_length=100,default=None,blank=True,null=True)
    TXNAMOUNT= models.DecimalField(max_digits=16,decimal_places=2,default=0)
    PAYMENTMODE= models.CharField(max_length=25,default=None,blank=True,null=True)
    CURRENCY= models.CharField(max_length=25,default=None,blank=True,null=True)
    TXNDATE= models.DateTimeField(default=datetime.now)
    STATUS= models.CharField(max_length=25,default=None,blank=True,null=True)
    RESPCODE= models.CharField(max_length=10,default=None,blank=True,null=True)
    RESPMSG= models.CharField(max_length=100,default=None,blank=True,null=True)
    GATEWAYNAME= models.CharField(max_length=100,default=None,blank=True,null=True)
    BANKTXNID= models.CharField(max_length=100,default=None,blank=True,null=True)
    BANKNAME=models.CharField(max_length=250,default=None,blank=True,null=True)