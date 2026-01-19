from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

from infrastructure.repositories import DjangoCustomerRepository, DjangoBookRepository, DjangoCartRepository
from usecases.customer_ops import RegisterCustomerUseCase, LoginCustomerUseCase
from usecases.book_ops import ListBooksUseCase
from usecases.cart_ops import AddToCartUseCase, ViewCartUseCase

# Wiring / Dependency Injection Helper
def get_customer_repo():
    return DjangoCustomerRepository()

def get_book_repo():
    return DjangoBookRepository()

def get_cart_repo():
    return DjangoCartRepository()

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        usecase = RegisterCustomerUseCase(get_customer_repo())
        try:
            usecase.execute(name, email, password)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except ValueError as e:
            return render(request, 'register.html', {'error': str(e)})
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        usecase = LoginCustomerUseCase(get_customer_repo())
        try:
            customer = usecase.execute(email, password)
            # Set session
            request.session['customer_id'] = customer.id
            return redirect('books')
        except ValueError as e:
            return render(request, 'login.html', {'error': str(e)})
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def book_catalog(request):
    usecase = ListBooksUseCase(get_book_repo())
    books = usecase.execute()
    return render(request, 'books.html', {'books': books})

def add_to_cart(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return redirect('login')
            
        book_id = int(request.POST.get('book_id'))
        quantity = int(request.POST.get('quantity', 1))

        usecase = AddToCartUseCase(get_cart_repo(), get_book_repo())
        try:
            usecase.execute(customer_id, book_id, quantity)
            messages.success(request, 'Thêm vào giỏ hàng thành công')
            return redirect('books') # Stay on catalog to continue shopping or go to cart? User usually likes staying.
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('books')
    return redirect('books')

def view_cart(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    usecase = ViewCartUseCase(get_cart_repo())
    cart = usecase.execute(customer_id)
    return render(request, 'cart.html', {'cart': cart})
