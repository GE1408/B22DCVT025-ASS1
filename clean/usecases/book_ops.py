from typing import List
from domain.entities import Book
from interfaces.repositories import BookRepository

class ListBooksUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def execute(self) -> List[Book]:
        return self.book_repo.list_all()
