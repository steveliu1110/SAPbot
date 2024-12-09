from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from django.http import JsonResponse, StreamingHttpResponse
import json
from .forms import SignupForm, LoginForm, WebsiteForm


from .models import Website, ChatSession, Message


from chatbot.custom.vstore import getVectorStore
from chatbot.custom.scraping import update_scrapy
from chatbot.custom.chatbot import answer_user_prompt

from chatbot.custom.historychat import answer

########################                  Test                    #############################


import time
@csrf_exempt
def test(request):
	def stream_generator():
		for i in range(10):
			yield f"Chunk {i} {time.strftime('%H:%M:%S')}\n"
			time.sleep(1)
		yield "Stream complete.\n"
	response = StreamingHttpResponse(stream_generator(), content_type='text/plain')
	response['Cache-Control'] = 'no-cache'
	return response


########################            Authentication              #############################
def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.save()
			messages.success(request, "Signup successful!")
			return redirect('login')
	else:
		form = SignupForm()
	
	return render(request, 'signup.html', {'form': form})


def login(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			return redirect('admindash')
		return redirect('home') 
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				auth.login(request, user)
				if user.is_superuser:
					return redirect('admindash')
				return redirect('home')  # Redirect to homepage or a dashboard
			else:
				messages.error(request, 'Invalid username or password.')
	else:
		form = LoginForm()

	return render(request, 'login.html', {'form': form})
##################################################################################################



########################            Rendering Dashboard              #############################

@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminDash(request):
	query = request.GET.get('search', '')
	sort = request.GET.get('sort', 'last_update')
	direction = request.GET.get('direction', 'asc')

	if direction == 'desc':
		sort = f"-{sort}"

	websites = Website.objects.filter(url__icontains=query).order_by(sort)

	paginator = Paginator(websites, 10)  # Show 10 websites per page
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'page_obj': page_obj,
		'query': query,
		'current_sort' : sort.lstrip('-'),
		'current_direction': direction,
		# 'form': form
	}
	return render(request, 'admindash.html', context)

@login_required
def home(request):
	chat_sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
	print(chat_sessions)
	return render(request, 'home.html', {
		'page' : 'home',
		'chat_sessions': chat_sessions,
		'messages' : []
	})

##################################################################################################



########################            Scraping Operation              #############################

@csrf_exempt  # Temporarily disable CSRF for the API endpoint (not recommended for production)
def add_websites(request):
	if request.method == 'POST':
		# Get the list of websites from the form data
		websites_text = request.POST.get('websites')
		# Split the websites string into a list of URLs (one per line)
		websites_text = websites_text.replace(" ", "")
		website_urls = [url.strip() for url in websites_text.split("\n")]
		result = 0
		# Add each website to the database
		for url in website_urls:

			if url == "":
				continue
			# You can customize this to add other data like chunk_count, last_update
			if not Website.objects.filter(url=url).exists():
				print('New url ' + url + 'added')
				Website.objects.create(url=url, chunk_count=0, last_update="Not Scraped Yet")
				result = result + 1
		
		# Return a success response (you can also return a JSON response or redirect if necessary)
		return JsonResponse({'status': True,'message': 'Selected websites updated successfully!', 'result' : result})
	
	return JsonResponse({'status': False,'message': 'Invalid request method'}, status=400)

@csrf_exempt  # Disable CSRF for simplicity, but use CSRF token in production
def update_websites(request):
	if request.method == 'POST':
		try:
			url = request.POST.get('website')
			result = update_scrapy(url)
			if result:
				instance = Website.objects.get(url=url)
				instance.chunk_count = result[2]
				instance.last_update = result[1]
				instance.save()
				print('Updating websites:', result, url)
				return JsonResponse({'status': True,'message': 'Selected websites updated successfully!', 'result' : result})
		except Exception as e:
			return JsonResponse({'status': False,'message': str(e)}, status=400)
	return JsonResponse({'status': False,'message': 'error occured'}, status=405)


##################################################################################################



########################            Chatbot Operation              #############################


@csrf_exempt  # Disable CSRF for simplicity, but use CSRF token in production
def ask_query(request):
	if request.method == 'POST':
		try:
			query = request.POST.get('query')
			session_id = request.POST.get('session_id')
			print('the query and session id are', query, session_id)
			chat_session = ChatSession.objects.get(session_id=session_id)
			message = Message.objects.create(chat_session=chat_session, role='user', content=query)
			message.save()
			vstore = getVectorStore()
			# response = answer_user_prompt(query, vstore)
			response = answer(query, session_id)
			return StreamingHttpResponse(response, content_type='text/event-stream')
		except Exception as e:
			return StreamingHttpResponse('some error while api', status=400)
	return StreamingHttpResponse('some error while api', status=400)

@csrf_exempt
def new_chat(request):
	if request.method == 'POST':
		try:
			query = request.POST.get('query')
			chat_session = ChatSession.objects.create(user=request.user)
			session_id = chat_session.session_id
			print('new session created! the session id is', chat_session.session_id)
			if query:
				message = Message.objects.create(chat_session=chat_session, role='user', content=query)
				message.save()

				vstore = getVectorStore()
				response = answer(query, session_id)
				return StreamingHttpResponse(response, content_type='text/event-stream')
		except Exception as e:
			return StreamingHttpResponse('some error while api' + str(e), status=400)
	return StreamingHttpResponse('some error while api', status=400)

@csrf_exempt
def getnewsession(request):
	if request.method == 'GET':
		try:
			chat_sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
			print('new session created! the session id is', chat_sessions[0].session_id)
			return JsonResponse({'status': True,'message': 'successfully deleted', 'session_id' : chat_sessions[0].session_id}, status=200)
		except Exception as e:
			return JsonResponse({'status': False,'message': 'error occured'}, status=400)
	return JsonResponse({'status': False,'message': 'error occured'}, status=405)

# @login_required
def chat_session(request, session_id):
	chat_sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
	chat_session = None
	try:
		chat_session = ChatSession.objects.get(session_id=session_id, user=request.user)
	except Exception:
		return redirect('home')

	messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')
	return render(request, 'home.html', {
		'page': 'chat',
		'messages': (messages), 
		'chat_sessions': chat_sessions,
		'session_id': chat_session.session_id
		})

########################            Handle Session              #############################

@csrf_exempt
def delete_session(request):
	if request.method == 'POST':
		try:
			session_id = request.POST.get('session_id')
			chat_session = ChatSession.objects.get(session_id=session_id)
			messages = Message.objects.filter(chat_session=chat_session)
			
			for msg in messages:
				msg.delete()
			chat_session.delete()
			
			return JsonResponse({'status': True,'message': 'successfully deleted'}, status=200)
		except Exception as e:
			return JsonResponse({'status': False,'message': 'error occured'}, status=400)
	return JsonResponse({'status': False,'message': 'error occured'}, status=405)






##################################################################################################