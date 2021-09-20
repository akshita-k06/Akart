from django.contrib import admin
from .models import product,contactdetails,orderdetails,ordertracker,OrderPayment
from django.utils.html import format_html

#admin.site.register(product)
#admin.site.register(contactdetails)
#admin.site.register(orderdetails)
#admin.site.register(ordertracker)

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    def ProductImage(self, object):
        return format_html('<img src="{}" width="80" />'.format(object.image.url))
    search_fields = ('product_name',)
    list_display = ("id","product_name","ProductImage")
    list_display_links = ('id','product_name','ProductImage')
    class Meta: 
        model=product

@admin.register(contactdetails)
class ContactDetailsAdmin(admin.ModelAdmin):
    search_fields = ('contact_name','contact_email','contact_phone')
    list_display = ("contact_id","contact_name","contact_email",'contact_phone')
    list_display_links = ('contact_id',"contact_name","contact_email")
    class Meta: 
        model=contactdetails

@admin.register(orderdetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    search_fields = ('ordername','orderemail')
    list_display = ("order_id","ordername","orderamount",'orderemail')
    list_display_links = ('order_id',"ordername","orderemail")
    class Meta: 
        model=orderdetails

@admin.register(ordertracker)
class OrderTrackerAdmin(admin.ModelAdmin):
    search_fields = ('update_id','order_id','update_desc','timestamp')
    list_display = ("update_id","order_id","update_desc",'timestamp')
    list_display_links = ("update_id","order_id","update_desc",'timestamp')
    class Meta: 
        model=ordertracker

@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    search_fields = ('id','order_id','TXNAMOUNT','PAYMENTMODE')
    list_display = ("id","order_id","TXNAMOUNT",'TXNID','TXNDATE')
    list_display_links = ("id","order_id","TXNAMOUNT",'TXNID')
    class Meta: 
        model=OrderPayment