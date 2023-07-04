from django.urls import path
from . import views

app_name = 'credential'

urlpatterns = [
    path("", views.login_view, name="login"),
    path("index/", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("fetch_tickers/", views.fetch_tickers, name="fetch_tickers"),
    path("buy_stock/", views.buy_stock, name="buy_stock"),
    path("buy_stock2/", views.buy_stock2, name="buy_stock2"),
    path("my_stocks/", views.Stock, name="my_stocks"),
    path("user/", views.user_view, name="user"),
    path('sell/<str:ticker_name>/', views.sell_stock, name='sell_stock'),

]