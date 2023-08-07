from uuid import uuid4
import uuid
from fastapi import FastAPI, HTTPException
import random
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class Book(BaseModel):
    name: str
    price: float
    genre: Literal["fiction", "non- fiction" ]
    book_id : Optional[str] = uuid4().hex



Book_file = "book.json"
BOOK_DATABASE = []

if os.path.exists(Book_file):
    with open(Book_file, 'r') as f:
        BOOK_DATABASE = json.load(f)


@app.get("/")
def home():
    return {"Message": "Welcome to my bookstore"}


# list of bookstores
@app.get("/list-of-books")
def list_of_books():
    return {"BookS": [BOOK_DATABASE]}


# get books by index
@app.get("/get-books-index/{index}")
def get_books_index(index: int):
    if index < 0 or index >= len(BOOK_DATABASE):
        raise HTTPException(404, f"Index out of range")
    else: 
      return {"BookS": [BOOK_DATABASE[index]]}
    
    

# get-random-book
@app.get('/get-random-book')
def get_random_book():
    return random.choice(BOOK_DATABASE)


# /add book
@app.post('/add-book')
def add_book(book: Book):
    book.book_id = uuid.uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    with open(Book_file, 'w') as f:
        json.dump(BOOK_DATABASE, f)
    return {"Message": f"Book {book} added successfully", "id": book.book_id}


# /get-books?book_id
@app.get('/get-books')
async def get_books(book_id: str):
    for book in BOOK_DATABASE:
        if book['book_id'] == book_id:
            return book
        
    raise HTTPException(404, f"Book not found: {book_id}")