import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product

products_data = [
    {
        'name': 'Royal Oud',
        'price': 240.00,
        'image_url': 'https://images.unsplash.com/photo-1615655406736-b37c4fabf923?q=80&w=2070&auto=format&fit=crop'
    },
    {
        'name': 'Gold Chrono',
        'price': 4200.00,
        'image_url': 'https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?q=80&w=1894&auto=format&fit=crop'
    },
    {
        'name': 'Navigator',
        'price': 350.00,
        'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=1887&auto=format&fit=crop'
    },
    {
        'name': 'Amber Absolute',
        'price': 310.00,
        'image_url': 'https://images.unsplash.com/photo-1595475207225-428b62bda831?q=80&w=2080&auto=format&fit=crop'
    },
    {
        'name': 'Fountain Pen',
        'price': 180.00,
        'image_url': 'https://images.unsplash.com/photo-1583265266432-154df077a28e?q=80&w=1974&auto=format&fit=crop'
    }
]

# Note: Django ImageField usually expects a file, but for this demo we might need to handle it differently
# if the user's template expects a URL.
# The template does: <img src="{{ product.imageURL }}">
# The model has:
# @property
# def imageURL(self):
#     try:
#         url = self.image.url
#     except:
#         url = ''
#     return url

# If we want to use external URLs, we might need to hack the model or store local files.
# BUT, looking at the code I replaced: `src="{{ product.imageURL }}"`.
# If I want to support external URLs, I should probably update the model to allow an external URL override, 
# OR just download these images.
# For now, to keep it simple and fix the immediate "empty" look, I will try to save these objects.
# But `product.image` is a FileField. I can't just put a string in it easily without downloading.

# ALTERNATIVE: Update the template to fallback to a custom field or just hack the `imageURL` property.
# Let's check `models.py` again.
# It has `image = models.ImageField(null=True, blank=True)`.

# I will update `models.py` to allow an external URL, or I'll just download the images in the script.
# Downloading is robust.

import requests
from django.core.files.base import ContentFile

# Delete existing products to force refresh
Product.objects.all().delete()
print("Deleted existing products")

for item in products_data:
    # Check if exists (Redundant now, but safer to remove)
    # if Product.objects.filter(name=item['name']).exists():
    #     print(f"Skipping {item['name']}")
    #     continue

    print(f"Creating {item['name']}")
    p = Product(name=item['name'], price=item['price'], digital=False)
    
    # Download image
    try:
        response = requests.get(item['image_url'])
        if response.status_code == 200:
            file_name = item['name'].lower().replace(' ', '_') + '.jpg'
            p.image.save(file_name, ContentFile(response.content), save=False)
    except Exception as e:
        print(f"Failed to download image: {e}")
    
    p.save()
    print(f"Saved {item['name']}")

