from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.routes import router as api_router, initialize_scraping
from app.core.redis import init_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup and cleanup on shutdown."""
    # Startup
    logger.info("Initializing Redis connection...")
    await init_redis()
    logger.info("Redis connection established, initializing scraping...")
    
    try:
        # Call the init endpoint function directly
        result = await initialize_scraping()
        logger.info(f"Scraping initialization completed: {result}")
    except Exception as e:
        logger.error(f"Error during scraping initialization: {str(e)}")
    
    logger.info("Application startup complete.")
    
    yield
    
    # Shutdown
    logger.info("Application shutdown complete.")

app = FastAPI(
    title="AI Virtual Assistant API",
    description="API for the AI-powered virtual assistant system",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 