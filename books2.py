from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    
    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(title = 'id is not needed!')
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length = 100)
    rating: int = Field(gt = 0, lt = 6)
    
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 'title': 'A new book',
    #                 'author': 'harish',
    #                 'description': 'A new book description',
    #                 'rating': 5
    #             }
    #         ]
    #     }
    # }
    
    class Config:
        # Adding a example schema in swagger
        # arbitrary_types_allowed = True
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'harish',
                'description': 'A new book description',
                'rating': 5
            }
        }
    

BOOKS = [
    Book(1, 'Ikigai', 'Hector Garcia', 'Feel Good Book!', 5),
    Book(2, 'The Alchemist', 'Paulo Coelho', 'A profound novel about finding one’s destiny', 4),
    Book(3, 'The Subtle Art of Not Giving a F*ck', 'Mark Manson', 'A counterintuitive approach to living a good life', 4.5),
    Book(4, 'Atomic Habits', 'James Clear', 'Transform your habits, transform your life', 5),
    Book(5, 'The Power of Now', 'Eckhart Tolle', 'A guide to spiritual enlightenment', 4.5),
    Book(6, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'Unveiling the story of Homo sapiens', 4.5)
]


@app.get('/books', status_code = status.HTTP_200_OK)
async def get_all_book():
    return BOOKS

@app.post('/books/create-book', status_code = status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    # .model_dump() converts class to dict, this is another way of .dict() method
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

@app.get('/books/{book_id}', status_code = status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code = 404, detail = 'Item not found')

@app.get('/books/', status_code = status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt = 0, lt = 6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    
    return books_to_return

@app.put('/books/update-book', status_code = status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code = 404, detail = 'Item not found')

@app.delete('/books/{book_id}',  status_code = status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
    if not book_changed:
        raise HTTPException(status_code = 404, detail = 'Item not found')

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    
    return book