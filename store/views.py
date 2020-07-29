from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime

from .forms import registerForm
from .models import *
from .decorators import unauthenticatedUser

# Create your views here.
@unauthenticatedUser
def register(request):

	form= registerForm()

	if request.method=='POST':
		form= registerForm(request.POST)

		if form.is_valid():
			user= form.save()

			username= form.cleaned_data.get('username')
			messages.success(request, 'Account has been created for' +username)

			Customer.objects.create(
				user=user,
				name=user.username,
				email= user.email,
				)

			return redirect('login_page')


	context={'form':form}

	return render(request, 'store/register.html', context)


@unauthenticatedUser
def loginPage(request):

	if request.method == 'POST':
		username= request.POST.get('username')
		password= request.POST.get('password')

		user=authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')

		else:
			messages.error(request, "username or password is incorrect")


	context={}

	return render(request, "store/login.html", context)


	

def logoutUser(request):
	logout(request)
	return redirect('login_page')




	

def store(request):
	if request.user.is_authenticated:
		customer= request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False) 
		items= order.orderitem_set.all()
		cartItems= order.get_cart_items

	else:
		items=[]
		order= {'get_cart_total': 0, 'get_cart_items':0, 'shipping': False }
		cartItems= order['get_cart_items']

	Products= Product.objects.all()

	context={'Products': Products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)





def cart(request):
	if request.user.is_authenticated:
		customer= request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False) 
		items= order.orderitem_set.all()
		cartItems= order.get_cart_items

	else:
		return redirect('login_page')

	context={'items':items, 'order': order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)





def checkout(request):

	if request.user.is_authenticated:
		customer= request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False) 
		items= order.orderitem_set.all()
		cartItems= order.get_cart_items

	else:
		return redirect('login_page')



	context={'items':items, 'order': order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)





def UpdateItem(request):
	data = json.loads(request.body)
	productId= data['productId']
	action= data['action']

	print('Action:', action)

	print('Product:', productId)

	customer= request.user.customer

	product = Product.objects.get(id=productId)

	order, created= Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity= (orderItem.quantity+1)

	elif action == 'remove':
		orderItem.quantity= (orderItem.quantity-1)

	orderItem.save()

	if orderItem.quantity<=0:
		orderItem.delete()


	return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
	transaction_id= datetime.datetime.now().timestamp()
	data= json.loads(request.body)
	if request.user.is_authenticated:
		customer= request.user.customer
		order, created= Order.objects.get_or_create(customer=customer, complete=False)
		total= float(data['form']['total'])
		order.transaction_id=transaction_id

		if total==order.get_cart_total:
			order.complete= True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer= customer,
				order= order,
				address= data['shipping']['address'],
				city= data['shipping']['city'],
				state= data['shipping']['state'],
				zipcode= data['shipping']['zipcode'],

				)

	else:
		return redirect('login_page')
	return JsonResponse('Payment Submitted...', safe=False)
