"""
GitHub-to-AD Account Mapping API
A FastAPI application for querying GitHub user-to-AD account mappings and access control.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.database import init_db
from app.routes import router

# Initialize database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="GitHub-to-AD Account Mapping API",
    description="Query GitHub accounts, groups, and repositories to determine AD account mappings and access levels",
    version="1.0.0",
    lifespan=lifespan
)

# Include routes
app.include_router(router)

@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/", tags=["root"])
def root():
    """API information endpoint"""
    return {
        "name": "GitHub-to-AD Account Mapping API",
        "version": "1.0.0",
        "documentation": "/docs",
        "openapi_schema": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
