from .views import login_view
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),          # Assuming you have a home view
    path('login/', views.login_view, name='login'),
    # Add the Contact Path
    path('contact/', views.contact, name='contact'),
    path('', views.home, name='home'),  # Assuming you have a home view
    path('wallet-terminal/', views.wallet_view, name='wallet_dashboard'),  # <--- ADD THIS

    # Placeholder paths for info/plan if you haven't made them yet
    # path('info/', views.info, name='info'),
    # path('plan/', views.plan, name='plan'),
]
# Note the name='login'
