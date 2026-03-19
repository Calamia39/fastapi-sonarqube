"""
FastAPI application with health check
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="FastAPI SonarQube Demo",
    description="API demo for SonarQube integration",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello World", "status": "ok"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "fastapi-app"
        },
        status_code=200
    )

@app.get("/api/users")
async def get_users():
    """Get users list"""
    return {
        "users": [
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Smith"}
        ]
    }

def calculate_sum(num1: int, num2: int) -> int:
    """Calculate sum of two numbers"""
    return num1 + num2

def divide_numbers(num1: float, num2: float) -> float:
    """Divide two numbers"""
    if num2 == 0:
        raise ValueError("Cannot divide by zero")
    return num1 / num2