from fastapi import FastAPI
from app.database import engine
from app import models

# Import routers
from app.auth.auth_routes import router as auth_router
from app.exam.question_routes import router as question_router
from app.exam.exam_routes import router as exam_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Hybrid AI Exam Engine")

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(question_router, prefix="/questions", tags=["Questions"])
app.include_router(exam_router, prefix="/exam", tags=["Exam Engine"])

# Root endpoint
@app.get("/")
def home():
    return {"message": "AI Exam Engine Running Successfully"}