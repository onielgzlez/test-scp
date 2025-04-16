from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

from app.core.redis import get_redis
from app.scrapers.scrape_books import scrape_books
from app.scrapers.scrape_hn import scrape_hn_headlines

router = APIRouter()

class BookResponse(BaseModel):
    id: str
    title: str
    price: float
    category: str
    image_url: str

class HeadlineResponse(BaseModel):
    title: str
    score: int
    url: str

@router.post("/init")
async def initialize_scraping():
    """Initialize book scraping and store in Redis."""
    try:
        redis = await get_redis()
        books = await scrape_books()
        for book in books:
            # Convert the book dictionary to JSON string
            await redis.set(f"book:{book['id']}", json.dumps(book))
        return {"message": "Scraping completed successfully", "books_count": len(books)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books/search")
async def search_books(
    title: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None
) -> List[BookResponse]:
    """Search books by title, category, and price."""
    try:
        redis = await get_redis()
        all_books = []
        
        # Get all book keys
        keys = await redis.keys("book:*")
        for key in keys:
            book_data = await redis.get(key)
            if book_data:
                book = BookResponse.model_validate_json(book_data)
                if (
                    (not title or title.lower() in book.title.lower()) and
                    (not category or category.lower() == book.category.lower()) and
                    (not max_price or book.price <= max_price)
                ):
                    all_books.append(book)
        
        return all_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books")
async def get_books(category: Optional[str] = None) -> List[BookResponse]:
    """Get all books, optionally filtered by category."""
    try:
        redis = await get_redis()
        all_books = []
        
        # Get all book keys
        keys = await redis.keys("book:*")
        for key in keys:
            book_data = await redis.get(key)
            if book_data:
                book = BookResponse.model_validate_json(book_data)
                if not category or category.lower() == book.category.lower():
                    all_books.append(book)
        
        return all_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/headlines")
async def get_headlines(limit: Optional[int] = None) -> List[HeadlineResponse]:
    """Get current Hacker News headlines.
    
    Args:
        limit: Optional parameter to limit the number of headlines returned.
    """
    try:
        headlines = await scrape_hn_headlines(limit=limit)
        return [HeadlineResponse(**headline) for headline in headlines]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))