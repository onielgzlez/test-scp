# AI-Powered Virtual Assistant System

A production-ready, containerized system that integrates modern AI-driven technologies into a cohesive, user-facing application. The system features a frontend virtual assistant that interacts with an n8n-powered backend to retrieve and process web-scraped data stored in Redis, served via a FastAPI backend.

## System Components

- **Web Scraping**: BeautifulSoup and Selenium for data extraction
  - Books data from books.toscrape.com
  - Real-time Hacker News headlines
- **Backend**: FastAPI with Redis storage
- **Workflow Automation**: n8n for AI agent integration
- **Frontend**: Modern web interface for user interaction

## Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- Node.js 16+ (for frontend development)

## Quick Start

1. Clone the repository
2. Run the system:
```bash
docker-compose up --build
```

The system will automatically:
- Initialize Redis
- Start the FastAPI backend
- Launch the n8n workflow automation
- Deploy the frontend interface
- Run initial book scraping

## Example Queries

- "Find me a book about science under £15"
- "Show me trending tech headlines"
- "What are the latest mystery books under £20?"

## Redis Schema

### Books
- Key format: `book:<id>`
- Value format: JSON object
```json
{
  "title": "Book Name",
  "price": 12.99,
  "category": "Fiction",
  "image_url": "https://..."
}
```

### Hacker News
- Real-time fetching, no permanent storage

## API Endpoints

### FastAPI Backend
- POST `/init`: Trigger initial book scraping
- GET `/books/search`: Search books by title or category
- GET `/headlines`: Fetch current Hacker News headlines

### n8n Webhook
- POST `/ask`: Process user queries and return combined results

## Testing

Run tests inside Docker containers:

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test
```

## Security Measures

- Input validation using Pydantic models
- Rate limiting on API endpoints
- Secure environment variable handling
- Container isolation
- HTTPS for all external communications

## Technical Decisions

- **Redis**: Chosen for fast in-memory data storage and caching
- **FastAPI**: Selected for async support and automatic API documentation
- **n8n**: Used for flexible workflow automation and AI agent integration
- **Docker**: Ensures consistent development and deployment environments 