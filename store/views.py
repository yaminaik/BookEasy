from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import auth
from subprocess import run,PIPE
from .models import *
from django.http import JsonResponse
import sys
import json 
import datetime
from .forms import RegisterForm,CustomerForm, SearchForm, CommentForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
import razorpay
from django.core.mail import send_mail 
from django.conf import settings 
from django.contrib import messages



def search(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		if request.method == 'POST':
			form =  SearchForm(request.POST)
			if form.is_valid():
				query = form.cleaned_data['query']
				products=Product.objects.filter(name=query)
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'products': products,'cartItems':cartItems}
	return render(request,'store/index.html',context)



def signup(request):
	if request.method == "POST":
		form=RegisterForm(request.POST)
		form1=CustomerForm(request.POST)
		if form.is_valid() and form1.is_valid():
			a=form.save()
			b=form1.save()
			b.user = a
			b.save()
			return redirect('/login')
	else:
		form=RegisterForm()
		form1=CustomerForm()
	return render(request,'store/signup.html', {'form':form , 'form1':form1})

def login(request):
	return render(request,'store/login.html')

def index(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	products = Product.objects.all()
	context = {'products': products,'cartItems':cartItems}
	return render(request,'store/index.html',context)

def about(request):
	return render(request,'store/about.html')

def success(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items =order.orderitem_set.all()
		cartItems = order.get_cart_items
		if request.method=="POST":
			orderId = request.POST.get('orderId')
			order = Order.objects.filter(id=orderId)
			if len(order)>0: 
				update =OrderInfo.objects.filter(order_id=orderId)
				updates = []
				for item in update:
					updates.append({'text':item.update_desc,'time':item.timestamp})
					response = json.dumps(updates, default=str)
					return HttpResponse(response)
		else:
			HttpResponse('error')
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	context = {'items':items, 'order':order,'cartItems':cartItems}
	return render(request,'store/success.html',context)

def contact(request):
	return render(request,'store/contact.html')


def book(request):
	return render(request,'store/book.html')


def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items =order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	context = {'items':items, 'order':order,'cartItems':cartItems}
	return render(request,'store/cart.html',context)


def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items =order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	context = {'items':items, 'order':order,'cartItems':cartItems} 
	return render(request,'store/checkout.html',context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	client = razorpay.Client(auth=("rzp_test_a6SQyxPY7IfF2e", "5fzOr2IQSN4NbOi6jQrcU161"))

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = int(float(data['form']['total']))
		total = total* 100
		payment = client.order.create({'amount':total,'currency':'INR','payment_capture':'1'})
		order.transaction_id = payment['id']
		if total == order.get_cart_total*100:
			order.complete = True
		order.save()

		if order.shipping == True:	
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
		update= OrderInfo(customer=customer,order_id= order.id, update_desc="The order has been placed",delievered=False)
		update.save()
		subject = 'Order Details'
		message = f'Hi {customer.name}, ThankYou for ordering from BookEasy.Your OrderID is {order.id}.' 
		recipient_list = [customer.email, ] 
		send_mail( subject, message, 'bookeasy21@gmail.com', recipient_list,fail_silently=False) 
	else:
		print('User is not logged in')
	return JsonResponse('Payment done',safe=False)

def product_detail(request,id):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items =order.orderitem_set.all()
		cartItems = order.get_cart_items
		product = Product.objects.get(pk=id)
		pcomments=Comment.objects.filter(product_id=id,ctype="Positive")
		a=pcomments.count()
		ncomments=Comment.objects.filter(product_id=id,ctype="Negative")
		b=ncomments.count()
		
		import pandas as pd
		import numpy as np
		import sys
		import string
		df=pd.read_csv("F://sem8//book_store//book_data2.csv")
		df.head()
		req=df.drop(columns=['book_authors','book_edition','book_format'])
		req.head()
		req.info()
		from sklearn.feature_extraction.text import TfidfVectorizer
		from sklearn.metrics.pairwise import linear_kernel
		books_tfidf = TfidfVectorizer(stop_words='english')
		req['book_desc'] = req['book_desc'].fillna('')
		tvf_matrix = books_tfidf.fit_transform(req['book_desc'])
		tvf_matrix
		tvf_matrix.shape
		from sklearn.metrics.pairwise import sigmoid_kernel
		sig=sigmoid_kernel(tvf_matrix, tvf_matrix)
		indices=pd.Series(req.index,index=req['book_title']).drop_duplicates()
		print(indices)
		id1=product.name
		print(id1)
		idx =indices[id1]
		print(idx)
		id1d=req['book_desc'].iloc[idx]
		id1i=req['image_url'].iloc[idx]
		id1g=req['genres'].iloc[idx]
		sig_scores =list(enumerate(sig[idx]))
		sig_scores =sorted(sig_scores, key=lambda x:x[1], reverse=True)
		sig_scores=sig_scores[1:6]
		book_indices= [i[0] for i in sig_scores] 
		out=req['book_title'].iloc[book_indices]
		out1=req['book_desc'].iloc[book_indices]
		out2=req['image_url'].iloc[book_indices]
		out3=req['genres'].iloc[book_indices]
		print(out)
		print(out1)
		print(out2)
		print(out3)
		from wordcloud import WordCloud, STOPWORDS 
		import matplotlib.pyplot as plt 
		final_comment_words = ''
		emotion_comment_list = ''
		stopwords = set(STOPWORDS)
		for val in pcomments,ncomments:
			val = str(val) 
			lower_case = val.lower()
			cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
			tokenized_words = cleaned_text.split()
			for word in tokenized_words:
				if word not in stopwords:
					final_comment_words+=word
				print(final_comment_words)
			with open('F://sem8//book_store//emotions.txt', 'r') as file:
				for line in file:
					clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
					word, emotion = clear_line.split(':')

					if word in final_comment_words:
						emotion_comment_list+=emotion
			print(emotion_comment_list)
		  
		wordcloud = WordCloud(width = 800, height = 800, 
		                background_color ='white', 
		                stopwords = stopwords, 
		                min_font_size = 10).generate(emotion_comment_list) 
		  
		# plot the WordCloud image                       
		plt.figure(figsize = (8, 8), facecolor = None) 
		plt.imshow(wordcloud) 
		plt.axis("off") 
		plt.tight_layout(pad = 0)
		wordcloud.to_file("F:/sem8/book_store/store/static/images/first_review.png")

	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'product': product,'pcomments':pcomments, 'a':a,'b':b,'ncomments':ncomments, 'items':items, 'order':order,'cartItems':cartItems,'display':id1,'idx':idx,'display1':id1d,'display2':id1i,'display3':id1g, 'out': out, 'out1': out1 , 'out2': out2, 'out3': out3} 
	return render(request,'store/product_detail.html',context)
	
	
	
def addcomment(request,id):
	url=request.META.get('HTTP_REFERER')
	if request.user.is_authenticated:
		customer = request.user.customer
		product = Product.objects.get(pk=id)
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
		import string
		from collections import Counter
		import matplotlib.pyplot as plt
		import nltk
	
		import pandas as pd 
		nltk.download('wordnet')
		nltk.download('vader_lexicon')
		from nltk.corpus import stopwords
		from nltk.sentiment.vader import SentimentIntensityAnalyzer
		from nltk.stem import WordNetLemmatizer
		from nltk.tokenize import word_tokenize
		# reading text file
		final_words = []
		lemma_words=[]
		emotion_list = []
		text = request.POST.get('comment')
		lower_case = text.lower()
		cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
		tokenized_words = cleaned_text.split()
		stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
		              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
		              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
		              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
		              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
		              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
		              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
		              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
		              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
		              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

		for word in tokenized_words:
		    if word not in stop_words:
        		final_words.append(word)

		for word in final_words:
		    word = WordNetLemmatizer().lemmatize(word)
		    lemma_words.append(word)

		
		with open('F://sem8//book_store//emotions.txt', 'r') as file:
		    for line in file:
		        clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
		        word, emotion = clear_line.split(':')

		        if word in final_words:
		            emotion_list.append(emotion)
		print(emotion_list)

		def sentiment_analyse(sentiment_text):
		    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
		    if request.method == 'POST':
		    	form = CommentForm(request.POST)
		    	if score['neg'] > score['pos']:
		    		type="Negative"
		    		if form.is_valid():
		    			Comment.objects.create(
						customer=customer,
						product=product,
						subject = form.cleaned_data['subject'],
						comment = form.cleaned_data['comment'],
						rate = form.cleaned_data['rate'],
						ctype=type,
						)
		    	elif score['neg'] < score['pos']:
		    		type="Positive"
		    		if form.is_valid():
			        	Comment.objects.create(
						customer=customer,
						product=product,
						subject = form.cleaned_data['subject'],
						comment = form.cleaned_data['comment'],
						rate = form.cleaned_data['rate'],
						ctype=type,
						)
		    	else:
		    		type="Neutral"
		    		if form.is_valid():
			        	Comment.objects.create(
						customer=customer,
						product=product,
						subject = form.cleaned_data['subject'],
						comment = form.cleaned_data['comment'],
						rate = form.cleaned_data['rate'],
						ctype=type,
						)
		sentiment_analyse(cleaned_text)
	return HttpResponseRedirect(url)

