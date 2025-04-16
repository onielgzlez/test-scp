import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_initialize_scraping(client: AsyncClient):
    response = await client.post("/init")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "books_count" in data
    assert data["message"] == "Scraping completed successfully"
    assert data["books_count"] > 0

@pytest.mark.asyncio
async def test_search_books(client: AsyncClient):
    # Test without filters
    response = await client.get("/books/search")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    if books:  # If we have books, validate their structure
        book = books[0]
        assert "id" in book
        assert "title" in book
        assert "price" in book
        assert "category" in book
        assert "image_url" in book

    # Test with filters
    response = await client.get("/books/search?max_price=20")
    assert response.status_code == 200
    filtered_books = response.json()
    assert isinstance(filtered_books, list)
    if filtered_books:
        for book in filtered_books:
            assert float(book["price"]) <= 20

@pytest.mark.asyncio
async def test_get_headlines(client: AsyncClient):
    response = await client.get("/headlines")
    assert response.status_code == 200
    headlines = response.json()
    assert isinstance(headlines, list)
    if headlines:  # If we have headlines, validate their structure
        headline = headlines[0]
        assert "title" in headline
        assert "score" in headline
        assert "url" in headline

@pytest.mark.asyncio
async def test_get_books(client: AsyncClient):
    # Test without category filter
    response = await client.get("/books")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    if books:  # If we have books, validate their structure
        book = books[0]
        assert "id" in book
        assert "title" in book
        assert "price" in book
        assert "category" in book
        assert "image_url" in book

    # Test with category filter
    response = await client.get("/books?category=fiction")
    assert response.status_code == 200
    filtered_books = response.json()
    assert isinstance(filtered_books, list)
    if filtered_books:
        for book in filtered_books:
            assert book["category"].lower() == "fiction" 