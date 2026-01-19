from typing import List, Optional
from domain.entities import Customer, Book, Cart, CartItem
from interfaces.repositories import CustomerRepository, BookRepository, CartRepository
from store.models import CustomerModel, BookModel, CartModel, CartItemModel

class DjangoCustomerRepository(CustomerRepository):
    def get_by_email(self, email: str) -> Optional[Customer]:
        try:
            model = CustomerModel.objects.get(email=email)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None

    def save(self, customer: Customer) -> Customer:
        model = CustomerModel(
            name=customer.name,
            email=customer.email,
            password=customer.password
        )
        if customer.id:
            model.id = customer.id
        model.save()
        return self._to_entity(model)
    
    def _to_entity(self, model: CustomerModel) -> Customer:
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password
        )

class DjangoBookRepository(BookRepository):
    def list_all(self) -> List[Book]:
        models = BookModel.objects.all()
        return [self._to_entity(m) for m in models]

    def get_by_id(self, book_id: int) -> Optional[Book]:
        try:
            model = BookModel.objects.get(id=book_id)
            return self._to_entity(model)
        except BookModel.DoesNotExist:
            return None
    
    def _to_entity(self, model: BookModel) -> Book:
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            price=float(model.price),
            stock=model.stock
        )

class DjangoCartRepository(CartRepository):
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        # Simplification: Assume 1 active cart per user or just get the latest
        try:
            cart_model = CartModel.objects.filter(customer_id=customer_id).last()
            if not cart_model:
                return None
            return self._to_entity(cart_model)
        except Exception: # Broad exception for safety in this rough impl
            return None

    def save(self, cart: Cart) -> Cart:
        # Saving cart itself (mainly for creation)
        # Note: Handling nested items save is complex here, keeping it simple
        model = CartModel(customer_id=cart.customer_id)
        if cart.id:
            model.id = cart.id
        model.save()
        return self._to_entity(model)

    def add_item(self, cart_id: int, book_id: int, quantity: int) -> CartItem:
        # If cart_id is None, we need to create a cart first! 
        # But this method signature assumes we're just adding item.
        # The UseCase logic I wrote might need adjustment or we handle creation here.
        # Actually my UseCase passed `cart.id if cart else None`.
        if cart_id is None:
             raise ValueError("Cart ID is required to add item")

        item, created = CartItemModel.objects.get_or_create(
            cart_id=cart_id, 
            book_id=book_id,
            defaults={'quantity': 0}
        )
        item.quantity += quantity
        item.save()
        
        # Helper to convert item back
        # Using a simplified conversion as we don't have full book details here without query
        # But for 'CartItem' entity we need the Book entity.
        return self._to_entity_item(item)

    def _to_entity(self, model: CartModel) -> Cart:
        items = [self._to_entity_item(item) for item in model.items.all()]
        return Cart(
            id=model.id,
            customer_id=model.customer_id,
            created_at=model.created_at,
            items=items
        )

    def _to_entity_item(self, model: CartItemModel) -> CartItem:
        # We need the book entity
        book_repo = DjangoBookRepository()
        book = book_repo._to_entity(model.book)
        return CartItem(
            id=model.id,
            book=book,
            quantity=model.quantity
        )
