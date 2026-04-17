import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.core.security import limiter

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for market data analysis and trade opportunity insights in India.",
)

# Add state limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint - Serve Frontend Dashboard
@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = Path(__file__).parent / "app" / "frontend" / "index.html"
    return index_path.read_text(encoding="utf-8")

# Rate limit the router by injecting it into router dependencies or applying per-route
# Wait, SlowAPI usually requires the @limiter.limit decorator directly on the endpoint.
# Since we have it in endpoints.py, we should import limiter there or pass it.
# To keep things simple, let's wrap the endpoint in endpoints.py or just declare limiter in core.

# Let's include the router
app.include_router(api_router, prefix="")

