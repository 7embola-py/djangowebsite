from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Customer, Order, OrderItem
import json

class StoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.customer = Customer.objects.create(user=self.user, name='Test User', email='test@test.com')
        self.product = Product.objects.create(name='Test Product', price=10.00, digital=False)

    def test_store_view_context(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].name, 'Test Product')

    def test_add_to_cart_authenticated(self):
        self.client.login(username='testuser', password='password')
        data = {'productId': self.product.id, 'action': 'add'}
        response = self.client.post(
            reverse('update_item'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'Item was added', 'cartItems': 1}
        )
        
        # Verify OrderItem creation
        order = Order.objects.get(customer=self.customer, complete=False)
        order_item = OrderItem.objects.get(order=order, product=self.product)
        self.assertEqual(order_item.quantity, 1)

    def test_add_to_cart_increment(self):
        self.client.login(username='testuser', password='password')
        # Add once
        data = {'productId': self.product.id, 'action': 'add'}
        self.client.post(reverse('update_item'), json.dumps(data), content_type='application/json')
        # Add again
        self.client.post(reverse('update_item'), json.dumps(data), content_type='application/json')
        
        order = Order.objects.get(customer=self.customer, complete=False)
        order_item = OrderItem.objects.get(order=order, product=self.product)
        self.assertEqual(order_item.quantity, 2)
