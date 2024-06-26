# main/views.py
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from main.forms import RegistrationForm, AccountAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from main.models import Account
from arweb.models import Product, Component
from django.utils import timezone
from arweb.forms import ComponentForm
from functools import wraps

def login_required_redirect_home(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_redirect_home
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        print(form.errors)  # Print form errors for debugging

        if form.is_valid():
            print("FORM VALID")

            user = form.save(commit=False)

            user.emp_id = form.cleaned_data.get('emp_id')

            if form.cleaned_data.get('is_admin'):
                print("\n\nTRUEEEE\n\n")
                user.is_admin = True
            else:
                print("\n\nFALSEEEEE\n\n")

                user.is_admin = False

            user.save()

            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            account = authenticate(email=email, password=raw_password)

            subject = username + ', your account has been created (Automated, do not reply)'
            message = 'Hi, ' + username + '\n\nWe are glad to tell you that ' + request.user.username + ' has successfully created an account for you.\nYou may now proceed to log in to the system using these credentials:\n\nEmail: ' + email + '\nPassword: ' + raw_password + '\n\n\nTHIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL'
            email_from = settings.EMAIL_HOST_USER
            send_mail( subject, message, email_from, [email] )
            
            return redirect('home')
        else:
            print("FORM INVALID")
            context['registration_form'] = form

    else: #GET_request
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'main/register.html', context)
    
def logout_view(request):
    if request.user.is_authenticated:
        request.user.is_online = False
        request.user.last_seen = timezone.now()
        request.user.save()

    logout(request)
    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    context = {}

    user = request.user

    if user.is_authenticated:
        return redirect("home")
    
    if request.method == 'POST':
        form = AccountAuthenticationForm(data = request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                user.is_online = True
                user.last_login = timezone.now()
                user.save()
                login(request, user)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'main/login.html', context)

@login_required_redirect_home
def home_view(request):
    context = {}
    
    if not request.user.is_authenticated:
        return redirect('login')
    elif not request.user.is_admin:
        context = {}
        products = Product.objects.all()
        context['products'] = products
    
    user = request.user
    context['user'] = user

    return render(request, 'main/home.html', context)

@login_required_redirect_home
def manage_products_view(request):
    context = {}

    products = Product.objects.all()
    context['products'] = products

    return render(request, 'main/manage_products.html', context)

@login_required_redirect_home
def manage_accounts_view(request):
    context = {}

    accounts = Account.objects.all()
    context['accounts'] = accounts

    return render(request, 'main/manageaccounts.html', context)

@login_required_redirect_home
def manage_component_view(request):
    context = {}

    components = Component.objects.all()
    context['components'] = components

    return render(request, 'main/manage_components.html', context)

@login_required_redirect_home
def add_component(request):
    submitted = False
    error = False
    context = {}
    form = ComponentForm(request.POST or None)

    if request.method == "POST":
        form = ComponentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_components')
        else:
            submitted = True
            error = True
        
    context['form'] = form
    context['submitted'] = submitted
    context['error'] = error
    
    return render(request, 'main/add_component.html', context)

@login_required_redirect_home
def component_details_view(request, name, component_id):
    print("component details")
    context = {}
    component = Component.objects.get(component_id=component_id)
    context['component'] = component
    return render(request, 'main/component_details.html', context)

@login_required_redirect_home
def update_component_view(request, component_id):
    context = {}
    component = Component.objects.get(component_id=component_id)
    form = ComponentForm(request.POST or None, instance=component)

    if form.is_valid():
        form.save()
        return redirect('manage_components')
    else:
        submitted = True
        error = True

    context['component'] = component
    context['form'] = form
    return render(request, 'main/update_components.html', context)

@login_required_redirect_home
def account_details_view(request, email):
    account = Account.objects.get(email=email)

    context = {}
    context['account'] = account

    return render(request, 'main/account_details.html', context)

@login_required_redirect_home
def my_account_view(request):
    user = request.user

    context = {}
    context['account'] = user

    return render(request, 'main/my_account.html', context)

@login_required_redirect_home
def product_details_view(request, name, product_id):
    context = {}
    product = Product.objects.get(product_id=product_id)
    steps = product.get_steps()
    steps = sorted(steps, key=lambda x: x.order)
    components = product.components

    context['product'] = product
    context['steps'] = steps
    context['components'] = components

    return render(request, 'main/product_details.html', context)


