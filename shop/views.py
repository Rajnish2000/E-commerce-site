from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate,ProductView
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum
MERCHANT_KEY = 'bKMfNxPPf_QdZppa'
# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # print(nSlides)
    allProds = []
    catprods = Product.objects.values("category","id")
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category= cat)
        n = len(prod)
        print(prod)
        nSlides = (n//4) + ceil((n/4) - (n//4))
        allProds.append([prod,range(1,nSlides),nSlides])

    # params = {"no_of_slide":nSlides,'range':range(1,nSlides),'product':products}
    # allProds = [[products,range(1,nSlides),nSlides],
    #             [products,range(1,nSlides),nSlides]];
    params = {"product" : allProds};
    return render(request,'shop/index.html',params)

def searchMatch(query ,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category:
        return True
    else:
        return False        


def search(request):
    query = request.GET.get('search');
    if len(query) > 150 or len(query) == 0:
    # post = []
        product = Product.objects.none()
        return render(request, 'shop/search.html',{'query':query})

    allProds = []
    catprods = Product.objects.values("category","id")
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodTemp = Product.objects.filter(category= cat)
        prod =[item for item in prodTemp if searchMatch(query,item)]
        n = len(prod)
        print(prod)
        nSlides = (n//4) + ceil((n/4) - (n//4))
        if len(prod) !=0:
            allProds.append([prod,range(1,nSlides),nSlides])
    params = {"product" : allProds,'msg':""}
    if len(allProds) == 0 or len(query) < 4 :
        params = {'msg':'please enter the revelant search query !','query':query}
    return render(request,'shop/search.html',params)        
    # return render(request, "shop/search.html");

def productPage():
    return render(request,'shop/product.html')

def about(request):
    return render(request,"shop/about.html")

def privacy(request):
    return render(request,'shop/privacy.html')

def team(request):
    return render(request,'shop/team.html')

def services(request):
    return render(request,'shop/services.html')

def contact(request):
    if request.method == "POST":
        print(request)
        name = request.POST.get("name" , "")
        email = request.POST.get("email" , "")
        phone = request.POST.get("phone" , "")
        desc = request.POST.get("desc" , "")
        # print(Name,Email,Phone,Desc)
        contact = Contact(Name=name,Email = email,Phone=phone,Desc = desc)
        contact.save()
    return render(request,"shop/contact.html");

def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId',"")
        email = request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id=orderId,email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                updates = []
                for items in update:
                    updates.append({'text':items.update_desc,'time':items.timestamp})
                    response = json.dumps({"status":'success',"updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{'status':'No items are here !'}")
        except Exception as e:
            return HttpResponse("{'status':'Error'}")
    return render(request, "shop/tracker.html");

def productview(request,prodid):
    # fetch the product using id
    product = Product.objects.filter(id=prodid)
    return render(request, "shop/productView.html",{"product":product[0]});

def checkout(request):
    if request.method == 'POST':
        print(request)
        name = request.POST.get('name','')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email','')
        address = request.POST.get('address','') + "  " + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip','')
        phone = request.POST.get('phone','')
        itemJSON = request.POST.get('itemJSON','')
        print(name,address,city,state,zip_code,phone)
        order = Orders(name=name,email=email,address=address,city= city,state=state,zip_code=zip_code,phone=phone,items_json = itemJSON,amount=amount)
        order.save()
        update = OrderUpdate(order_id = order.order_id,update_desc='the order has been placed successfully')
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank,'id': id})

        #request paytm to transfer the amount to your account after payment by user
        param_dict={
# WorldP64425807474247
            'MID': 'dcZRCd63955400650914',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

    }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return  render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request,'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # here patym will send you request
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


# superuser  : rajnish
# passeord : rajnish2000
# pooja di MID : dcZRCd63955400650914
# WorldP64425807474247