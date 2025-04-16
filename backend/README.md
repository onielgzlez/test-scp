# AI Virtual Assistant Backend

A FastAPI backend for the AI Virtual Assistant application that provides book search and Hacker News headlines functionality.

## Features

- Book search with filtering by title, category, and price
- Real-time Hacker News headlines
- Redis caching for book data
- Automated testing with pytest
- Swagger UI documentation

## API Documentation

Once the server is running, you can access the Swagger UI documentation at:
```
http://localhost:18000/docs
```

### Endpoints

#### Initialize Scraping
```
POST /init
```
Initializes the book scraping process and stores the data in Redis.

#### Search Books
```
GET /books/search
```
Search for books with optional filters:
- `title`: Filter by book title
- `category`: Filter by book category
- `max_price`: Filter by maximum price

#### Get Headlines
```
GET /headlines
```
Get current Hacker News headlines.

## Development Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the development server:
```bash
poetry run start
```

## Testing

Run the test suite:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=app
```

## Dependencies

- FastAPI
- Redis
- BeautifulSoup4
- Selenium
- Pytest
- Httpx

See `pyproject.toml` for complete dependency list. 