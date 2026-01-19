import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean.settings')
django.setup()

from store.models import BookModel

def populate():
    print("Populating data...")
    if BookModel.objects.count() > 0:
        print("Books already exist. Skipping population.")
        return

    books = [
        BookModel(title="Clean Architecture", author="Robert C. Martin", price=35.00, stock=10),
        BookModel(title="The Pragmatic Programmer", author="Andrew Hunt", price=40.00, stock=5),
        BookModel(title="Design Patterns", author="Erich Gamma", price=45.00, stock=8),
        BookModel(title="Refactoring", author="Martin Fowler", price=38.00, stock=3),
    ]
    
    BookModel.objects.bulk_create(books)
    print(f"Created {len(books)} books.")

if __name__ == '__main__':
    try:
        populate()
    except Exception as e:
        print(f"Error populating: {e}")
