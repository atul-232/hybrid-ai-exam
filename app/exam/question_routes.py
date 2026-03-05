from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Question
from app.utils.encryption import encrypt, decrypt

router = APIRouter()

# ---------------------------------
# Upload Question (Encrypted)
# ---------------------------------
@router.post("/upload")
def upload_question(subject: str, topic: str, difficulty: int, question: str):

    db = SessionLocal()

    encrypted_question = encrypt(question)

    new_question = Question(
        subject=subject,
        topic=topic,
        difficulty=difficulty,
        encrypted_content=encrypted_question
    )

    db.add(new_question)
    db.commit()

    return {
        "message": "Question stored securely"
    }


# ---------------------------------
# Get All Questions (Decrypted)
# ---------------------------------
@router.get("/")
def get_questions():

    db = SessionLocal()

    questions = db.query(Question).all()

    result = []

    for q in questions:
        result.append({
            "id": q.id,
            "subject": q.subject,
            "topic": q.topic,
            "difficulty": q.difficulty,
            "question": decrypt(q.encrypted_content)
        })

    return result