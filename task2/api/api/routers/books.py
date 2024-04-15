from fastapi import APIRouter, Depends, Path, status
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from .. import schemas
from ..dependencies import book_in_stock, get_db
from ..dependencies import get_book as get_book_dependency
from ..models.books import Book, BookFilter

router = APIRouter()

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Book], operation_id="getBooks")
def get_books(
    book_filter: BookFilter = FilterDepends(BookFilter),
    db: Session = Depends(get_db),
) -> list[schemas.Book]:
    db_books: list[Book] = Book.get_books(db, book_filter)
    books: list[schemas.Book] = [b.to_pydantic_model() for b in db_books]
    return books


@router.get("/{bookId}", status_code=status.HTTP_200_OK, response_model=schemas.Book, operation_id="getBook")
def get_book(
    book_id: int = Path(alias="bookId"),
    db: Session = Depends(get_db),
    db_book: Book = Depends(get_book_dependency),
) -> schemas.Book:
    return db_book.to_pydantic_model()


@router.post(
    "/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
    operation_id="addBook",
)
def add_book(info: schemas.BookInfo, db: Session = Depends(get_db)) -> schemas.Book:
    db_book: Book = Book.add_book(db=db, book_info=info)
    return db_book.to_pydantic_model()


@router.post(
    "/{bookId}",
    response_model=schemas.Book,
    responses={status.HTTP_404_NOT_FOUND: {"model": schemas.Detail}},
    operation_id="sellBook",
)
def sell_book(
    book_id: int = Path(alias="bookId"),
    db: Session = Depends(get_db),
    db_book: Book = Depends(book_in_stock),
) -> schemas.Book:
    db_book.sell_book(db=db)
    return db_book.to_pydantic_model()
