import asyncio
import hashlib
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

class BookScraper:
    def __init__(self):
        self.base_url = "https://books.toscrape.com"
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_page(self, url: str) -> str:
        """Fetch a page with retry logic."""
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise

    async def get_book_details(self, book_url: str) -> Optional[Dict]:
        """Get all book details from its individual page."""
        try:
            html = await self.fetch_page(book_url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Obtener todos los datos del libro de una vez
            title = soup.select_one('.product_main h1').text.strip()
            price = float(soup.select_one('.price_color').text.replace('£', ''))
            category = soup.select_one('.breadcrumb > li:nth-child(3) > a').text.strip()
            image_url = urljoin(self.base_url, soup.select_one('#product_gallery img')['src'])
            
            # Generate a unique ID using the title
            book_id = hashlib.md5(title.encode()).hexdigest()
            
            return {
                "id": book_id,
                "title": title,
                "price": price,
                "category": category,
                "image_url": image_url,
            }
        except Exception as e:
            logger.error(f"Error obteniendo detalles del libro {book_url}: {str(e)}")
            return None

    async def parse_book(self, book_element) -> Optional[Dict]:
        """Parse a book element into a dictionary."""
        try:
            title_elem = book_element.select_one("h3 a")
            price_elem = book_element.select_one(".price_color")
            image_elem = book_element.select_one("img")
            
            if not all([title_elem, price_elem, image_elem]):
                logger.warning("Missing required elements in book")
                return None
                
            title = title_elem["title"]
            price = float(price_elem.text.replace("£", ""))
            image_url = urljoin(self.base_url, image_elem["src"])
            
            # Obtener la categoría solo si el precio es menor al máximo permitido
            if price <= settings.MAX_BOOK_PRICE:
                book_url = urljoin(self.base_url, '/catalogue/' + title_elem["href"])
                html = await self.fetch_page(book_url)
                soup = BeautifulSoup(html, 'html.parser')
                category = soup.select_one('.breadcrumb > li:nth-child(3) > a').text.strip()
            else:
                return None
            
            # Generate a unique ID using the title
            book_id = hashlib.md5(title.encode()).hexdigest()
            
            return {
                "id": book_id,
                "title": title,
                "price": price,
                "category": category,
                "image_url": image_url,
            }
        except Exception as e:
            logger.error(f"Error parsing book: {str(e)}")
            return None

    async def scrape_books(self) -> List[Dict]:
        """Scrape books from multiple pages."""
        books = []
        current_page = 1
        
        while len(books) < settings.MAX_BOOKS_TO_SCRAPE:
            url = f"{self.base_url}/catalogue/page-{current_page}.html"
            try:
                html = await self.fetch_page(url)
                soup = BeautifulSoup(html, "html.parser")
                book_elements = soup.select(".product_pod")
                
                if not book_elements:
                    logger.info(f"No more books found on page {current_page}")
                    break
                
                for element in book_elements:
                    book = await self.parse_book(element)
                    if book and book["price"] <= settings.MAX_BOOK_PRICE:
                        books.append(book)
                        if len(books) >= settings.MAX_BOOKS_TO_SCRAPE:
                            break
                
                current_page += 1
            except Exception as e:
                logger.error(f"Error scraping page {current_page}: {str(e)}")
                break
        
        return books

async def scrape_books() -> List[Dict]:
    """Main function to scrape books."""
    async with BookScraper() as scraper:
        return await scraper.scrape_books() 