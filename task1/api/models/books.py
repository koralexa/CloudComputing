from __future__ import annotations

from typing import List, Optional, cast

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, Query, Session, mapped_column

from .. import schemas
from ..database import Base


class Book(Base):
    __tablename__ = "Books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int] = mapped_column(Integer)

    def to_pydantic_model(self) -> schemas.Book:
        return schemas.Book(
            id=self.id,
            name=self.name,
            author=self.author,
            quantity=self.quantity,
        )

    @classmethod
    def get_book(cls, db: Session, book_id: int) -> Book | None:
        book: Book | None = db.query(Book).get(book_id)
        db.commit()
        return book

    @classmethod
    def get_book_by_name_and_author(cls, db: Session, name: str, author: str) -> Book | None:
        book: Book | None = db.query(Book).filter_by(name=name, author=author).first()
        db.commit()
        return book

    @classmethod
    def get_books(cls, db: Session, book_filter: BookFilter, skip: int = 0, limit: int = 100) -> list[Book]:
        q: Query[Book] = db.query(Book)
        q = cast(Query[Book], book_filter.sort(book_filter.filter(q)))
        books: list[Book] = q.all()
        db.commit()
        return books

    @classmethod
    def add_book(cls, db: Session, book_info: schemas.BookInfo) -> Book:
        existing_book: Book | None = Book.get_book_by_name_and_author(
            db=db,
            name=book_info.name,
            author=book_info.author,
        )
        if existing_book is None:
            db_book: Book = Book(
                name=book_info.name,
                author=book_info.author,
                quantity=1,
            )
            db.add(db_book)
            db.commit()
            return db_book
        else:
            existing_book.quantity += 1
            db.commit()
            return existing_book

    def sell_book(self, db: Session) -> None:
        self.quantity -= 1
        db.commit()


class BookFilter(Filter):
    search: Optional[str]
    orderBy: List[str] = ["name"]  # noqa: N815

    class Constants(Filter.Constants):
        model = Book
        search_model_fields = ["name", "author"]
        ordering_field_name = "orderBy"
