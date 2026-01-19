import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean.settings')
django.setup()

from django.test import RequestFactory
from store.views import book_catalog

def debug_view():
    factory = RequestFactory()
    request = factory.get('/books/')
    
    print("\n--- Debugging Book Catalog View ---")
    try:
        response = book_catalog(request)
        print(f"Status: {response.status_code}")
        print(f"Content: {response.content.decode()}")
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    debug_view()
