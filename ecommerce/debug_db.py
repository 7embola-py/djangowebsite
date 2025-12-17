import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product, Customer
from django.contrib.auth.models import User

print(f'Products: {Product.objects.count()}')
print(f'Users: {User.objects.count()}')
print(f'Customers: {Customer.objects.count()}')

for user in User.objects.all():
    try:
        print(f'User: {user.username}, Customer: {user.customer}')
    except:
        print(f'User: {user.username}, Customer: NONE')
