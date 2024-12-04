from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from django.http import JsonResponse, StreamingHttpResponse
import json
from .forms import SignupForm, LoginForm, WebsiteForm


from .models import Website


from chatbot.custom.vstore import getVectorStore
from chatbot.custom.scraping import update_scrapy
from chatbot.custom.chatbot import answer_user_prompt

from chatbot.custom.historychat import answer


def website_list(request):
    query = request.GET.get('search', '')  # Get search query from the URL
    websites = Website.objects.filter(url__icontains=query)  # Filter by URL
    paginator = Paginator(websites, 10)  # Show 10 websites per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admindash.html', {'page_obj': page_obj, 'search_query': query})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminDash(request):
    # Fetch all Website entries from the database
    websites = Website.objects.all()

    # Check if the form is submitted to add a new website
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = WebsiteForm()

    return render(request, 'admindash.html', {
        'websites': websites,
        'form': form
    })

@login_required
def home(request):
    websites = [
        {'name': 'Example', 'url': 'https://example.com'},
        {'name': 'Google', 'url': 'https://google.com'},
        {'name': 'Twitter', 'url': 'https://twitter.com'},
        {'name': 'GitHub', 'url': 'https://github.com'},
    ]

    return render(request, 'home.html', {'websites': websites})

@csrf_exempt  # Temporarily disable CSRF for the API endpoint (not recommended for production)
def add_websites(request):
    if request.method == 'POST':
        # Get the list of websites from the form data
        websites_text = request.POST.get('websites')
        print(websites_text)
        # Split the websites string into a list of URLs (one per line)
        websites_text = websites_text.replace(" ", "")
        website_urls = [url.strip() for url in websites_text.split("\n")]
        print(website_urls,'wewe')
        # Add each website to the database
        for url in website_urls:

            if url == "":
                continue
            # You can customize this to add other data like chunk_count, last_update
            print(url, '----')
            if not Website.objects.filter(url=url).exists():
                Website.objects.create(url=url, chunk_count=0, last_update="Not Scraped Yet")
        
        # Return a success response (you can also return a JSON response or redirect if necessary)
        return JsonResponse({'message': 'Websites added successfully'})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

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

@csrf_exempt  # Disable CSRF for simplicity, but use CSRF token in production
def ask_query(request):
    if request.method == 'POST':
        try:
            query = request.POST.get('query')
            
            print('the query is', query)
            vstore = getVectorStore()
            # response = answer_user_prompt(query, vstore)
            response = answer(query, request.user.username)
            return StreamingHttpResponse(response, content_type='text/event-stream')
        except Exception as e:
            return StreamingHttpResponse('some error while api', status=400)
    return StreamingHttpResponse('some error while api', status=400)

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
