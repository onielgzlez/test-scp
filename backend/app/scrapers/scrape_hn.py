import asyncio
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from loguru import logger

from app.core.config import settings

class HackerNewsScraper:
    def __init__(self):
        self.base_url = "https://news.ycombinator.com"
        self.driver = None

    async def __aenter__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Use remote Selenium
        self.driver = webdriver.Remote(
            command_executor=f"http://{settings.REMOTE_DRIVER_URL}:{settings.REMOTE_DRIVER_PORT}/wd/hub",
            options=options
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def parse_story(self, element) -> Optional[Dict]:
        """Parse a story element into a dictionary."""
        try:
            # Obtener el elemento siguiente que contiene el score
            next_tr = element.find_element(By.XPATH, "following-sibling::tr[1]")
            score_elem = next_tr.find_element(By.CSS_SELECTOR, ".score")
            score = int(score_elem.text.split()[0])
            
            title_elem = element.find_element(By.CSS_SELECTOR, ".titleline a")
            title = title_elem.text
            url = title_elem.get_attribute("href")
            
            return {
                "title": title,
                "score": score,
                "url": url,
            }
        except Exception as e:
            logger.error(f"Error parsing story: {str(e)}")
            return None

    async def scrape_headlines(self, limit: Optional[int] = None) -> List[Dict]:
        """Scrape headlines from multiple pages.
        
        Args:
            limit: Optional parameter to limit the number of headlines returned.
        """
        headlines = []
        current_page = 1
        
        while current_page <= settings.HN_PAGES_TO_SCRAPE:
            if limit is not None and len(headlines) >= limit:
                break
                
            url = f"{self.base_url}/news?p={current_page}" if current_page > 1 else self.base_url
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".athing"))
                )
                
                story_elements = self.driver.find_elements(By.CSS_SELECTOR, ".athing")
                for element in story_elements:
                    if limit is not None and len(headlines) >= limit:
                        break
                        
                    story = self.parse_story(element)
                    if story:
                        headlines.append(story)
                
                current_page += 1
            except TimeoutException:
                logger.error(f"Timeout while loading page {current_page}")
                break
            except Exception as e:
                logger.error(f"Error scraping page {current_page}: {str(e)}")
                break
        
        return headlines

async def scrape_hn_headlines(limit: Optional[int] = None) -> List[Dict]:
    """Main function to scrape Hacker News headlines.
    
    Args:
        limit: Optional parameter to limit the number of headlines returned.
    """
    async with HackerNewsScraper() as scraper:
        return await scraper.scrape_headlines(limit) 