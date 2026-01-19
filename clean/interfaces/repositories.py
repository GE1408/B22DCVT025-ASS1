from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Customer, Book, Cart, CartItem

class CustomerRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        pass

class BookRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Book]:
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass

class CartRepository(ABC):
    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        pass

    @abstractmethod
    def save(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    def add_item(self, cart_id: int, book_id: int, quantity: int) -> CartItem:
        pass
