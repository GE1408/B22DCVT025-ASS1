from datetime import datetime
from domain.entities import Cart, CartItem
from interfaces.repositories import CartRepository, BookRepository

class AddToCartUseCase:
    def __init__(self, cart_repo: CartRepository, book_repo: BookRepository):
        self.cart_repo = cart_repo
        self.book_repo = book_repo

    def execute(self, customer_id: int, book_id: int, quantity: int) -> Cart:
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        if book.stock < quantity:
            raise ValueError("Insufficient stock")

        cart = self.cart_repo.get_by_customer_id(customer_id)
        if not cart:
            # Create new cart logic
            new_cart = Cart(
                id=None, 
                customer_id=customer_id, 
                created_at=datetime.now(), 
                items=[]
            )
            cart = self.cart_repo.save(new_cart)
        
        self.cart_repo.add_item(cart_id=cart.id, book_id=book_id, quantity=quantity)
        
        return self.cart_repo.get_by_customer_id(customer_id)

class ViewCartUseCase:
    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    def execute(self, customer_id: int) -> Cart:
        return self.cart_repo.get_by_customer_id(customer_id)
