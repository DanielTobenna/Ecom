from django.urls import path

from . import views

urlpatterns=[

	path('', views.store, name='store'),
	path('cart/', views.cart, name='cart'),
	path('checkout/', views.checkout, name='checkout'),
	path('update_item/', views.UpdateItem, name='update_item'),
	path('process_order/', views.processOrder, name='process_order'),
	path('register/', views.register, name='register'),
	path('login_page/', views.loginPage, name='login_page'),
	path('logout_page/', views.logoutUser, name='logout_page'),

]

