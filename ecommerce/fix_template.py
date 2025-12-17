import re

# Read the file
with open(r'c:\Users\ASMAA\Desktop\cursor\ecommerce\store\templates\store\checkout.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the split template tag
content = content.replace(
    '<span class="font-serif text-3xl text-taylor-gold italic">${{\r\n                                order.get_cart_total|floatformat:2 }}</span>',
    '<span class="font-serif text-3xl text-taylor-gold italic">${{ order.get_cart_total|floatformat:2 }}</span>'
)

# Also try with just \n
content = content.replace(
    '<span class="font-serif text-3xl text-taylor-gold italic">${{\n                                order.get_cart_total|floatformat:2 }}</span>',
    '<span class="font-serif text-3xl text-taylor-gold italic">${{ order.get_cart_total|floatformat:2 }}</span>'
)

# Write back
with open(r'c:\Users\ASMAA\Desktop\cursor\ecommerce\store\templates\store\checkout.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("File fixed successfully!")
