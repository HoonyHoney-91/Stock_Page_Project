from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm
from django.contrib.auth.models import User
from .finance import get_stock_price_chart
from .buystock import get_buy_stock_user, get_buy_stock_user2
from .models import PurchasedStock, Stock
from decimal import Decimal
from itertools import chain

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return redirect('credential:user')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("credential:index"))
        else:
            return render(request, "users/login.html", {
                "message": "invalid credentials"
            })
    return render(request, "credential/login.html")

def logout_view(request):
    logout(request)
    return render(request, "credential/login.html",{
        "message": "Logged Out"
    })

def signup(request):
    template = 'credential/signup.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            else:

                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                login(request, user)

                return HttpResponseRedirect(reverse("credential:login"))
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})

@login_required
def fetch_tickers(request):
    if request.method == 'GET':
        search_term = request.GET.get('search_term')
        try:
            stock_price_chart = get_stock_price_chart(search_term)
            request.session['stock_price_chart'] = stock_price_chart
            return redirect('credential:user')
        except:
            error_message = "Name of the stock ticker does not exist"
            return render(request, 'credential/user.html', {'error_message': error_message})

@login_required
def buy_stock(request):
    if request.method == 'GET':
        stock_name = request.GET.get('stock_name')
        try:
            current_price, short_name = get_buy_stock_user(stock_name)
            request.session['stock_name'] = short_name
            request.session['current_price'] = current_price
            return redirect('credential:user')
        except:
            error_message = "Name of the stock ticker does not exist"
            return redirect('credential:user', error_message=error_message)

@login_required
def buy_stock2(request):
    if request.method == 'GET':
        stock_name = request.GET.get('stock_name')
        quantity = request.GET.get('quantity')
        try:
            if quantity:
                short_name_2, current_price_2 = get_buy_stock_user2(stock_name)

                if short_name_2 is None or current_price_2 is None:
                    # Stock ticker does not exist
                    error_message = "Name of the stock ticker does not exist"
                    return render(request, 'credential/user.html', {'error_message': error_message})

                # Retrieve existing purchased stocks for the current user
                user_stocks = PurchasedStock.objects.filter(user=request.user, stock_name=short_name_2, ticker_name=stock_name)

                if user_stocks.exists():
                    # If the user already has stocks of the same short name and ticker name, update the average price and quantity
                    existing_quantity = sum([stock.quantity for stock in user_stocks])
                    existing_total_price = sum([stock.quantity * stock.price for stock in user_stocks])

                    new_average_price = (existing_total_price + (Decimal(str(current_price_2)) * Decimal(str(quantity)))) / (existing_quantity + Decimal(str(quantity)))

                    existing_stock = user_stocks.first()
                    existing_stock.quantity += int(quantity)
                    existing_stock.price = new_average_price
                    existing_stock.save()
                else:
                    # If the user doesn't have any stocks of the same short name and ticker name, create a new PurchasedStock object
                    purchased_stock = PurchasedStock(
                        user=request.user,
                        stock_name=short_name_2,
                        ticker_name=stock_name,
                        quantity=quantity,
                        price=current_price_2
                    )
                    purchased_stock.save()

                return redirect('credential:user')
            else:
                error_message = "Number of stocks to purchase has not been selected"
                return render(request, 'credential/user.html', {'error_message': error_message})
        except Exception as e:
            error_message = f"An error occurred during the stock purchase: {str(e)}"
            return render(request, 'credential/user.html', {'error_message': error_message})

@login_required
def sell_stock(request, ticker_name):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        
        # Retrieve the stock object from the database
        stock = get_object_or_404(PurchasedStock, ticker_name=ticker_name)
        
        # Check if the quantity to sell is valid
        if quantity <= 0 or quantity > stock.quantity:
            messages.error(request, 'Invalid quantity to sell.')
        else:
            # Calculate new stock information
            new_quantity = stock.quantity - quantity
            
            # Check if the quantity becomes zero
            if new_quantity == 0:
                stock.delete()  # Remove the stock from the database if quantity becomes zero
            else:
                # Update average price and total value
                stock.price = ((stock.price * stock.quantity) - (stock.price * quantity)) / new_quantity
                stock.total_value = stock.price * new_quantity
                
                stock.quantity = new_quantity
                stock.save()
            
            messages.success(request, 'Stock sold successfully.')
    
    return redirect('credential:user')


@login_required
def user_view(request):
    user_stocks = PurchasedStock.objects.filter(user=request.user)
    print(user_stocks)
    options_lists = []
    for stock in user_stocks:
        stock.total_value = stock.quantity * stock.price
        stock_options = [(i+1) for i in range(stock.quantity)]
        options_lists.append(stock_options)
    stock_price_chart = request.session.get('stock_price_chart')
    stock_name = request.session.get('stock_name')
    current_price = request.session.get('current_price')
    context = {
        'user_stocks': user_stocks,
        'options_lists': options_lists
    }
    if stock_price_chart:
        context['stock_price_chart'] = stock_price_chart
    if stock_name and current_price:
        context['stock_name'] = stock_name
        context['current_price'] = current_price

    return render(request, 'credential/user.html', context)