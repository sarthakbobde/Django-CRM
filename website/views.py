from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddRecordForm
from django.contrib import messages
from .models import Record
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
    records = Record.objects.all()
    
    # checking login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,  f'{username}, you have been logged in!')
            return redirect('home')
        else:
            messages.success(request, "There was as error while logging in")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logout")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Sucessfully Registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
        
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request, "Record Deleted Sucessfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()                
                messages.success(request, "Record Added Sucessfully")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
    
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=record)
    if request.user.is_authenticated:
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In")
        return redirect('home')
    
def search_record(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        records = Record.objects.all()
        if request.user.is_authenticated:
            if query:
            #records = Record.objects.all().filter(first_name=query)
                records = records.filter(
                    first_name__icontains=query
                ) | records.filter(
                    last_name__icontains = query
                )  | records.filter(
                    email__icontains = query
                )  | records.filter(
                    phone__icontains = query
                )
            else:
                records = Record.objects.all()
            return render(request, 'home.html', {'records':records})
        else:
            messages.success(request, "You Must Be Logged In")
            return redirect('home')