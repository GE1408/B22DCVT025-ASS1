from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Seed the database with sample books'

    def handle(self, *args, **kwargs):
        # Clear existing books
        Book.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing books'))

        # Sample books data
        books_data = [
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'description': 'A Handbook of Agile Software Craftsmanship. Even bad code can function. But if code is not clean, it can bring a development organization to its knees.',
                'price': 32.99,
                'isbn': '9780132350884',
                'stock': 50,
                'category': 'Programming',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/41xShlnTZTL._SX376_BO1,204,203,200_.jpg'
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt, David Thomas',
                'description': 'Your Journey To Mastery. Written as a series of self-contained sections and filled with classic and fresh anecdotes, thoughtful examples, and interesting analogies.',
                'price': 41.45,
                'isbn': '9780135957059',
                'stock': 30,
                'category': 'Programming',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/41BKx1AxQWL._SX396_BO1,204,203,200_.jpg'
            },
            {
                'title': 'Design Patterns',
                'author': 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides',
                'description': 'Elements of Reusable Object-Oriented Software. Capturing decades of experience, this book provides a catalog of simple and succinct solutions to commonly occurring design problems.',
                'price': 54.99,
                'isbn': '9780201633612',
                'stock': 25,
                'category': 'Programming',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/51szD9HC9pL._SX395_BO1,204,203,200_.jpg'
            },
            {
                'title': 'Introduction to Algorithms',
                'author': 'Thomas H. Cormen, Charles E. Leiserson',
                'description': 'Some books on algorithms are rigorous but incomplete; others cover masses of material but lack rigor. Introduction to Algorithms uniquely combines rigor and comprehensiveness.',
                'price': 89.99,
                'isbn': '9780262033848',
                'stock': 20,
                'category': 'Computer Science',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/41T0iBxY8FL._SX440_BO1,204,203,200_.jpg'
            },
            {
                'title': 'Python Crash Course',
                'author': 'Eric Matthes',
                'description': 'A Hands-On, Project-Based Introduction to Programming. Python Crash Course is a fast-paced, thorough introduction to programming with Python.',
                'price': 39.95,
                'isbn': '9781593279288',
                'stock': 45,
                'category': 'Python',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/51XQKZ0oM5L._SX376_BO1,204,203,200_.jpg'
            },
            {
                'title': 'JavaScript: The Good Parts',
                'author': 'Douglas Crockford',
                'description': 'Most programming languages contain good and bad parts, but JavaScript has more than its share of the bad, having been developed and released in a hurry before it could be refined.',
                'price': 29.99,
                'isbn': '9780596517748',
                'stock': 35,
                'category': 'JavaScript',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/5166ztGa+SL._SX381_BO1,204,203,200_.jpg'
            },
            {
                'title': 'Head First Design Patterns',
                'author': 'Eric Freeman, Elisabeth Robson',
                'description': 'A Brain-Friendly Guide. At any given moment, someone struggles with the same software design problems you have.',
                'price': 44.99,
                'isbn': '9780596007126',
                'stock': 28,
                'category': 'Programming',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/51S8rrLoW+L._SX430_BO1,204,203,200_.jpg'
            },
            {
                'title': 'Eloquent JavaScript',
                'author': 'Marijn Haverbeke',
                'description': 'A Modern Introduction to Programming. This is a book about JavaScript, programming, and the wonders of the digital.',
                'price': 33.99,
                'isbn': '9781593279509',
                'stock': 40,
                'category': 'JavaScript',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/51IKylClGbL._SX376_BO1,204,203,200_.jpg'
            },
            {
                'title': 'You Do Not Know JS',
                'author': 'Kyle Simpson',
                'description': 'Up and Going. It is easy to learn parts of JavaScript, but much harder to learn it completely or even sufficiently.',
                'price': 24.99,
                'isbn': '9781491924464',
                'stock': 50,
                'category': 'JavaScript',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/41jZiPPqVjL._SX379_BO1,204,203,200_.jpg'
            },
            {
                'title': 'Automate the Boring Stuff with Python',
                'author': 'Al Sweigart',
                'description': 'Practical Programming for Total Beginners. Learn how to use Python to write programs that do in minutes what would take you hours to do by hand.',
                'price': 34.99,
                'isbn': '9781593279929',
                'stock': 55,
                'category': 'Python',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/51SxcN+v9qL._SX376_BO1,204,203,200_.jpg'
            }
        ]

        # Create books
        created_count = 0
        for book_data in books_data:
            book = Book.objects.create(**book_data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} books'))
