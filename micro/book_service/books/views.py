from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer, BookListSerializer, BookCreateSerializer


class BookListView(APIView):
    """API endpoint to list all books"""
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.all()
        
        # Optional filtering by category
        category = request.query_params.get('category', None)
        if category:
            books = books.filter(category__icontains=category)
        
        # Optional filtering by availability
        in_stock = request.query_params.get('in_stock', None)
        if in_stock and in_stock.lower() == 'true':
            books = books.filter(stock__gt=0)
        
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookDetailView(APIView):
    """API endpoint to get book details"""
    permission_classes = [AllowAny]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({
                'error': 'Book not found'
            }, status=status.HTTP_404_NOT_FOUND)


class BookCreateView(APIView):
    """API endpoint to create a new book"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            book_data = BookSerializer(book).data
            
            return Response({
                'message': 'Book created successfully',
                'book': book_data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckStockView(APIView):
    """API endpoint to check stock availability"""
    permission_classes = [AllowAny]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            quantity = int(request.query_params.get('quantity', 1))
            
            return Response({
                'book_id': book.id,
                'title': book.title,
                'stock': book.stock,
                'requested_quantity': quantity,
                'available': book.has_sufficient_stock(quantity)
            }, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({
                'error': 'Book not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'error': 'Invalid quantity parameter'
            }, status=status.HTTP_400_BAD_REQUEST)
