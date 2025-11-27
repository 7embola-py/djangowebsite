from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import datetime, timedelta


# This is the view that handles the /login/ url
def login_view(request):
    # This looks for login.html inside the templates folder
    return render(request, 'login.html')

def home(request):
    return render(request, 'voltage.html')

def contact(request):
    transmission_sent = False  # Flag to track success

    if request.method == "POST":
        # 1. Get data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # 2. Format the email content
        subject = f"VOLTAGE TRANSMISSION from {name}"
        full_message = f"SENDER: {name}\nFREQUENCY: {email}\n\nDATA PACKET:\n{message}"

        # 3. Send the email (From, To)
        # Replace 'your-email@gmail.com' with your actual receiving address
        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,  # From (your server)
            ['your-email@gmail.com'],  # To (you)
            fail_silently=False,
        )

        transmission_sent = True

    return render(request, 'contact.html', {'transmission_sent': transmission_sent})


def wallet_view(request):
    # Simulate a wallet address
    wallet_id = "0x7F" + "".join([random.choice("0123456789ABCDEF") for _ in range(16)]) + "K9"

    # Generate fake transaction history (The Lore)
    transactions = [
        {"type": "SMART_CONTRACT", "hash": "0x3a...9f", "val": "-0.045 ETH", "status": "CONFIRMED", "color": "red"},
        {"type": "MINING_REWARD", "hash": "0x1b...22", "val": "+1.200 VLT", "status": "RECEIVED", "color": "green"},
        {"type": "DARK_POOL_SWAP", "hash": "0x9c...aa", "val": "+5000 USDT", "status": "ENCRYPTED", "color": "blue"},
        {"type": "GAS_FEE", "hash": "0x00...00", "val": "-0.002 ETH", "status": "BURNED", "color": "grey"},
    ]

    context = {
        'wallet_id': wallet_id,
        'transactions': transactions,
        'balance': "8,420,069.00",  # The fake "Whale" balance
    }
    return render(request, 'wallet.html', context)