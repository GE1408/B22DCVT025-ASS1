import urllib.request
import urllib.parse
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def verify_http():
    print("Waiting for server...")
    time.sleep(3) # Give runserver time to start
    
    # 1. View Catalog
    print("\n--- 1. View Catalog ---")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/books/") as response:
            data = json.load(response)
            print(f"Books: {len(data['books'])}")
            if not data['books']:
                print("No books found.")
                return
            book_id = data['books'][0]['id']
            print(f"Target Book ID: {book_id}")
    except Exception as e:
        print(f"FAIL: {e}")
        return

    # 2. Register
    print("\n--- 2. Register ---")
    reg_data = urllib.parse.urlencode({
        'name': 'HTTP User',
        'email': 'http@example.com', 
        'password': 'password123'
    }).encode()
    try:
        req = urllib.request.Request(f"{BASE_URL}/register/", data=reg_data, method='POST')
        with urllib.request.urlopen(req) as response:
            print(f"Register status: {response.status}")
            print(f"Response: {response.read().decode()}")
    except urllib.error.HTTPError as e:
        print(f"Register failed (might already exist): {e.code} {e.read().decode()}")

    # 3. Login & Session
    print("\n--- 3. Login ---")
    login_data = urllib.parse.urlencode({
        'email': 'http@example.com', 
        'password': 'password123'
    }).encode()
    
    cj = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(cj)
    
    try:
        req = urllib.request.Request(f"{BASE_URL}/login/", data=login_data, method='POST')
        with opener.open(req) as response:
            print(f"Login status: {response.status}")
            print(f"Response: {response.read().decode()}")
            
        # 4. Add to Cart (using opener with cookies)
        print("\n--- 4. Add to Cart ---")
        cart_data = urllib.parse.urlencode({'book_id': book_id, 'quantity': 1}).encode()
        req = urllib.request.Request(f"{BASE_URL}/cart/add/", data=cart_data, method='POST')
        with opener.open(req) as response:
            print(f"Add status: {response.status}")
            
        # 5. View Cart
        print("\n--- 5. View Cart ---")
        req = urllib.request.Request(f"{BASE_URL}/cart/")
        with opener.open(req) as response:
            data = json.load(response)
            print(f"Cart items: {len(data.get('items', []))}")
            
    except Exception as e:
        print(f"FAIL: {e}")

if __name__ == '__main__':
    verify_http()
