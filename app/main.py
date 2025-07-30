from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ai

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include AI router
app.include_router(ai.router)

from app.routes import market

app.include_router(market.router)
