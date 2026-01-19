import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean.settings')
django.setup()

from django.test import Client

def verify_full_flow():
    # raise_request_exception=True makes the Client raise exceptions instead of returning 500 responses
    client = Client(raise_request_exception=True)
    
    print("\n--- 1. View Catalog ---")
    try:
        response = client.get('/books/')
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Books found: {len(data['books'])}")
        if len(data['books']) == 0:
            print("No books found, skipping cart test.")
            return
        book_id = data['books'][0]['id']
    except Exception:
        print("Crash in View Catalog:")
        traceback.print_exc()
        return

    print("\n--- 2. Register Customer ---")
    email = "debug_user@example.com"
    password = "password123"
    try:
        # We allow 400 if user exists
        response = client.post('/register/', {'name': 'Debug User', 'email': email, 'password': password})
        print(f"Register status: {response.status_code}")
    except Exception:
        print("Crash in Register:")
        traceback.print_exc()
        return

    print("\n--- 3. Login ---")
    try:
        response = client.post('/login/', {'email': email, 'password': password})
        print(f"Login status: {response.status_code}")
        print(f"Response: {response.content.decode()}")
        if response.status_code == 200:
            print("Login successful.")
        else:
            print("Login failed.")
            return
    except Exception:
        print("Crash in Login:")
        traceback.print_exc()
        return

    print("\n--- 4. Add to Cart ---")
    try:
        response = client.post('/cart/add/', {'book_id': book_id, 'quantity': 1})
        print(f"Add to cart status: {response.status_code}")
        print(f"Response: {response.content.decode()}")
    except Exception:
        print("Crash in Add to Cart:")
        traceback.print_exc()
        return

    print("\n--- 5. View Cart ---")
    try:
        response = client.get('/cart/')
        print(f"View cart status: {response.status_code}")
        cart_data = response.json()
        print(f"Cart items: {len(cart_data.get('items', []))}")
    except Exception:
        print("Crash in View Cart:")
        traceback.print_exc()

if __name__ == '__main__':
    verify_full_flow()
