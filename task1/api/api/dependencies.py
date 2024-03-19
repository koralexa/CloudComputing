from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models.books import Book


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_book(
    book_id: int = Path(alias="bookId"),
    db: Session = Depends(get_db),
) -> Book:
    book: Book | None = Book.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


async def book_in_stock(
    book_id: int = Path(alias="bookId"),
    db: Session = Depends(get_db),
    book: Book = Depends(get_book),
) -> Book:
    if book.quantity == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not in stock")
    return book
