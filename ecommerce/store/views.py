from http.client import HTTPResponse

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import datetime
from .models import *
from django.core.paginator import Paginator

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems = 0
        
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request,'store/store.html',context)
def cart(request):
    # 1. Check if user is logged in
    if request.user.is_authenticated:
        customer = request.user.customer
        # 2. Get the user's un-finished order
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # 3. Get all the items inside that order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # If not logged in, show empty cart (we will fix Guest login later)
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request,'store/checkout.html',context)



def updateItem(request):
    # 1. Parse the data sent from Javascript
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    # 2. Get the customer and product
    customer = request.user.customer
    product = Product.objects.get(id=productId)

    # 3. Get or Create the Order
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # 4. Get or Create the specific Item in the order
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # 5. Do the Math (+1 or -1)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    # 6. If quantity is 0, delete the item
    if orderItem.quantity <= 0:
        orderItem.delete()

    # 7. Get new cart items count
    cartItems = order.get_cart_items

    return JsonResponse({'message': 'Item was added', 'cartItems': cartItems}, safe=False)


def heritage(request):
    context = {}
    return render(request, 'store/heritage.html', context)


def journal(request):
    # 1. Ask the database for ALL posts
    posts = Post.objects.all()

    # 2. Put them in a context dictionary so HTML can use them
    context = {'posts': posts}

    # 3. Send them to the template
    return render(request, 'store/journal.html', context)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.complete:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted..', safe=False)


def shop(request):
    # 1. Get all products (ordered by ID so they don't jump around)
    product_list = Product.objects.all().order_by('id')

    # 2. Setup Pagination: Show 9 products per page
    paginator = Paginator(product_list, 9)

    # 3. Get the current page number from the URL
    page_number = request.GET.get('page')

    # 4. Get the specific chunk of products
    products = paginator.get_page(page_number)

    context = {'products': products}
    return render(request, 'store/shop.html', context)

