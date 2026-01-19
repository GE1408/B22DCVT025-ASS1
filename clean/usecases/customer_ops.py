from domain.entities import Customer
from interfaces.repositories import CustomerRepository

class RegisterCustomerUseCase:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    def execute(self, name: str, email: str, password: str) -> Customer:
        # In real world: check if email exists, hash password
        existing = self.customer_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        
        new_customer = Customer(id=None, name=name, email=email, password=password)
        return self.customer_repo.save(new_customer)

class LoginCustomerUseCase:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    def execute(self, email: str, password: str) -> Customer:
        customer = self.customer_repo.get_by_email(email)
        if not customer:
            raise ValueError("Invalid credentials")
        if customer.password != password: # Should verify hash
            raise ValueError("Invalid credentials")
        return customer
