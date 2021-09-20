from django.shortcuts import render
from django.http import HttpResponse
from .models import product, contactdetails, orderdetails, ordertracker,OrderPayment
import json
from django.views.decorators.csrf import csrf_exempt
from .PaytmChecksum import generate_checksum,verify_checksum
# Create your views here.
from math import ceil
from datetime import datetime
# import PaytmChecksum


MERCHANT_KEY='G8EG7M#BhKqHVgY7'

def index(request):
    allproducts=[]
    catprods= product.objects.values('subcatagory', 'id')
    cats= {item["subcatagory"] for item in catprods}
    for i in cats:
        newproducts=product.objects.filter(subcatagory=i)
        n=len(newproducts)
        slides=(n//4)+ceil((n/4)-(n//4))
        print(type(newproducts))
        allproducts.append([newproducts, range(1,slides), slides, i])
    params={'allproducts': allproducts}
    return render(request,'akart/index.html',params)
def searchmatch(query,item):
    if query in item.product_description or query in item.catagory or query in item.subcatagory or query in item.product_name:
        return True
    else:
        return False
def search(request):
    query=request.GET.get('search')
    allproducts=[]
    catprods= product.objects.values('subcatagory', 'id')
    cats= {item["subcatagory"] for item in catprods}
    for i in cats:
        temp=product.objects.filter(subcatagory=i)
        searchitem=[item for item in temp if searchmatch(query, item)]
        n=len(searchitem)
        slides = n // 4 + ceil((n / 4) - (n // 4))
        if len(searchitem)!= 0:
            allproducts.append([searchitem, range(1, slides), slides,i])
        msg=""
    if len(allproducts)==0:
        msg="Please make sure to enter relevant search query"
    params={'allproducts':allproducts,"msg":msg}
    return render(request,'akart/search.html',params) 

def about(request):
    return render(request,'akart/about.html')
def track(request):
    if request.method=="POST":
       
        trackerid=request.POST.get('trackerid','')
        trackerpassword=request.POST.get('trackerpassword','')
       
        try:
            orderlen=orderdetails.objects.filter(order_id=trackerid)
            print(orderlen)
            print(orderlen[0].items_json)
            if len(orderlen)>0:
                update_list=[]
                update=ordertracker.objects.filter(order_id=trackerid)
                for item in update:
                    update_list.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps({"status":"success","updates":update_list,"itemjson":orderlen[0].items_json},default=str)
                    print(response)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            print(e)
            return HttpResponse('{}')
    return render(request,'akart/track.html')  
def productview(request,myid):
    #fetching product using id
    fetchproduct=product.objects.filter(id=myid)
    print(fetchproduct)
    return render(request,'akart/productview.html',{'recproduct':fetchproduct[0]})
 
def cart(request):
    return HttpResponse("AKSHITA")
def check(request):
    if request.method=="POST":
        try:
            items_json= request.POST.get('items_json', '')
            print(items_json)
            ordername=request.POST.get('ordername','')
            orderamount=request.POST.get('orderamount','')
            orderaddress=request.POST.get('orderaddress','')
            orderaddress1=request.POST.get('orderaddress1','')
            ordercontact=request.POST.get('ordercontact','')
            ordercontact1=request.POST.get('ordercontact1','')
            ordercity=request.POST.get('ordercity','')
            orderstate=request.POST.get('orderstate','')
            orderpincode=request.POST.get('orderpincode','')
            orderemail=request.POST.get('orderemail','')
            orderpassword=request.POST.get('orderpassword','')
            funorder = orderdetails(items_json=items_json,ordername=ordername,orderamount=orderamount,orderaddress=orderaddress,orderaddress1=orderaddress1,ordercontact=ordercontact,ordercontact1=ordercontact1,ordercity=ordercity,orderstate=orderstate,orderpincode=orderpincode,orderemail=orderemail,orderpassword=orderpassword)
            funorder.save()
            track=ordertracker(order_id=funorder,update_desc="The order has been placed")
            track.save()
            thank=True
            sendid=funorder.order_id
            params={'revid':sendid,'recthank':thank}
            # Request paytm to transfer the amount to your account after payment by user
            param_dict = {
                'MID': 'KmrLlj76715026113257',
                'ORDER_ID': str(funorder.order_id),
                'TXN_AMOUNT': str(orderamount),
                'CUST_ID': orderemail,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/akart/handlepaytm/',
            }
            param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, MERCHANT_KEY)
            return render(request,'akart/paytm.html',{'paytm_dict':param_dict})
            # return render(request, 'akart/check.html',params)
        except Exception as e:
            print(e)
    return render(request,'akart/check.html') 

@csrf_exempt
def handlepaytm(request):
    #paytm post request will be handled here 
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = verify_checksum(response_dict, MERCHANT_KEY, checksum)
    op = OrderPayment(
        order_id = orderdetails(response_dict['ORDERID']),
        TXNID = response_dict['TXNID'],
        TXNAMOUNT = response_dict['TXNAMOUNT'],
        PAYMENTMODE = response_dict['PAYMENTMODE'],
        CURRENCY = response_dict['CURRENCY'],
        TXNDATE = response_dict['TXNDATE'],
        STATUS = response_dict['STATUS'],
        RESPCODE = response_dict['RESPCODE'],
        RESPMSG = response_dict['RESPMSG'],
        GATEWAYNAME = response_dict['GATEWAYNAME'],
        BANKTXNID = response_dict['BANKTXNID'],
        BANKNAME = response_dict['BANKNAME']
    )
    op.save()

    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    # return HttpResponse('done')
    return render(request, 'akart/paymentstatus.html', {'response': response_dict})    

def contact(request):
    thank=False
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        feedback=request.POST.get('feedback','')
        tempcontact=contactdetails(contact_name=name, contact_email=email, contact_phone=phone, contact_feedback=feedback)
        tempcontact.save()
        thank=True
    return render(request,'akart/contact.html',{'thank':thank})