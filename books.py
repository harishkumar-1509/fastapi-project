from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'category': 'maths', 'author': 'Author One', 'title': 'Title One'},
    {'category': 'maths', 'author': 'Author Two', 'title': 'Title Two'},
    {'category': 'science', 'author': 'Author Three', 'title': 'Title Three'},
    {'category': 'maths', 'author': 'Author Four', 'title': 'Title Four'},
]

@app.get('/books')
async def get_all_books():
    return BOOKS

@app.get('/books/my-book')
async def get_my_book():
    return {'title':'My Favourite Book!'}

# path paramter
@app.get('/books/{book_title}')
async def get_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

# query paramters
@app.get('/books/')
async def get_book_by_category(category: str):
    book_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            book_to_return.append(book)
    return book_to_return

# both path and query parameters
@app.get('/books/{book_author}/')
async def get_book_by_category_and_author(book_author:str, category: str):
    book_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold() and book.get('author').casefold() == book_author.casefold():
            book_to_return.append(book)
    return book_to_return

@app.post('/books/create-book')
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

@app.put('/books/update-book')
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

@app.delete('/books/delete-book/{book_title}')
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break