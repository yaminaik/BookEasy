from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('registration/login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('success/', views.success, name='success'),
 	path('index/search/', views.search, name='search'),
    path('index/search/product/<int:id>/',views.product_detail,name='product_detail'),
    path('index/search/product/<int:id>/addcomment/',views.addcomment,name='addcomment'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('book/', views.book, name='book'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update/', views.updateItem, name='update'),
    path('process/', views.processOrder, name='process'),
    path('index/product/<int:id>/',views.product_detail,name='product_detail'),
    path('index/product/<int:id>/addcomment/',views.addcomment,name='addcomment')
   
]
 