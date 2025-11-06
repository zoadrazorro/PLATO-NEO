"""
Metaluminous Engine - FastAPI Web Application
"""
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from ..models import GenerationRequest, DebateSession, PhilosophicalDomain
from ..core import MetaluminousEngine
from ..config import settings


# Initialize engine
engine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI"""
    global engine
    logger.info("Starting Metaluminous Engine...")
    engine = MetaluminousEngine()
    yield
    logger.info("Shutting down Metaluminous Engine...")


# Create FastAPI app
app = FastAPI(
    title="Metaluminous Engine API",
    description="Computational Philosophy Engine for generating and refining novel philosophical positions",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Metaluminous Engine",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/generate", response_model=DebateSession)
async def generate_position(
    request: GenerationRequest,
    use_cloud_apis: bool = False,
):
    """
    Generate and critique a philosophical position.
    
    Args:
        request: GenerationRequest with problem and parameters
        use_cloud_apis: Whether to use cloud APIs (Four Sages Council)
        
    Returns:
        DebateSession with complete analysis
    """
    try:
        logger.info(f"Received generation request: {request.problem[:100]}")
        session = await engine.process_problem(request, use_cloud_apis=use_cloud_apis)
        return session
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explore", response_model=List[DebateSession])
async def explore_problem(
    request: GenerationRequest,
    num_variations: int = 10,
):
    """
    Explore the problem space with multiple variations.
    
    Args:
        request: GenerationRequest with problem and parameters
        num_variations: Number of variations to generate (1-50)
        
    Returns:
        List of DebateSessions sorted by quality
    """
    if num_variations < 1 or num_variations > 50:
        raise HTTPException(
            status_code=400,
            detail="num_variations must be between 1 and 50"
        )
    
    try:
        logger.info(f"Exploring problem space with {num_variations} variations")
        sessions = await engine.explore_problem_space(
            request,
            num_variations=num_variations,
            use_cloud_apis=False,  # Exploration uses local models only
        )
        return sessions
    except Exception as e:
        logger.error(f"Exploration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/domains", response_model=List[str])
async def list_domains():
    """List available philosophical domains"""
    return [domain.value for domain in PhilosophicalDomain]


@app.get("/config")
async def get_config():
    """Get current configuration (sensitive values masked)"""
    return {
        "ollama_host": settings.ollama_host,
        "ollama_primary_model": settings.ollama_primary_model,
        "ollama_critic_model": settings.ollama_critic_model,
        "ollama_creative_model": settings.ollama_creative_model,
        "max_iterations": settings.max_iterations,
        "novelty_threshold": settings.novelty_threshold,
        "min_testable_predictions": settings.min_testable_predictions,
        "cloud_apis_configured": {
            "openai": settings.openai_api_key is not None,
            "anthropic": settings.anthropic_api_key is not None,
            "google": settings.google_api_key is not None,
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting Metaluminous Engine on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        "metaluminous.web.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
