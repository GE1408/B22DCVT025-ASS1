import os
import django
import json
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean.settings')
django.setup()

from django.test import Client

def verify_flow():
    client = Client()
    
    print("\n--- 1. View Catalog ---")
    try:
        response = client.get('/books/')
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Content: {response.content}")
        else:
            data = response.json()
            print(f"Books found: {len(data['books'])}")
            if len(data['books']) == 0:
                print("FAIL: No books found")
                return
            global book_id
            book_id = data['books'][0]['id']
    except Exception:
        traceback.print_exc()
        return

    print("\n--- 2. Register Customer ---")
    email = "test@example.com"
    password = "password123"
    try:
        response = client.post('/register/', {'name': 'Test User', 'email': email, 'password': password})
        print(f"Register status: {response.status_code}")
        print(f"Content: {response.content}")
    except Exception:
        traceback.print_exc()

    print("\n--- 3. Login ---")
    try:
        response = client.post('/login/', {'email': email, 'password': password})
        print(f"Login status: {response.status_code}")
        if response.status_code != 200:
            print(f"FAIL: Login failed. Content: {response.content}")
            return
    except Exception:
        traceback.print_exc()
        return
    
    print("\n--- 4. Add to Cart ---")
    try:
        response = client.post('/cart/add/', {'book_id': book_id, 'quantity': 1})
        print(f"Add to cart status: {response.status_code}")
        print(f"Response: {response.content.decode()}")
    except Exception:
        traceback.print_exc()

    print("\n--- 5. View Cart ---")
    try:
        response = client.get('/cart/')
        print(f"View cart status: {response.status_code}")
        cart_data = response.json()
        print(f"Cart items: {len(cart_data.get('items', []))}")
        if len(cart_data.get('items', [])) > 0:
            print("SUCCESS: Items found in cart")
        else:
            print("FAIL: Cart is empty")
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    verify_flow()
