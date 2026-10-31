from fastapi import FastAPI

app = FastAPI(
    title="AI TestBench",
    description="Behavior-First AI Assurance Platform",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to AI TestBench",
        "status": "operational",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI TestBench API",
    }