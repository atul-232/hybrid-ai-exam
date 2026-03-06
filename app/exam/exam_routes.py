from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Question
from app.utils.encryption import decrypt
from app.ai.blueprint import generate_blueprint
from app.ai.generator import generate_coulomb_question
import random
from app.exam.risk_engine import calculate_risk
from app.analytics.analytics_engine import calculate_result
from app.analytics.feedback_engine import generate_feedback
from app.models import ExamSession
router = APIRouter()

# ---------------------------------
# Generate Exam with Blueprint + AI
# ---------------------------------

@router.post("/generate")
def generate_exam(subject: str, num_questions: int):

    db = SessionLocal()

    # Generate blueprint
    blueprint = generate_blueprint(num_questions)

    easy_q = blueprint["easy"]
    medium_q = blueprint["medium"]
    hard_q = blueprint["hard"]

    # Fetch questions from DB
    easy_questions = db.query(Question).filter(
        Question.subject == subject,
        Question.difficulty == 1
    ).all()

    medium_questions = db.query(Question).filter(
        Question.subject == subject,
        Question.difficulty == 2
    ).all()

    hard_questions = db.query(Question).filter(
        Question.subject == subject,
        Question.difficulty == 3
    ).all()

    # Shuffle questions
    random.shuffle(easy_questions)
    random.shuffle(medium_questions)
    random.shuffle(hard_questions)

    # Select based on blueprint
    selected_questions = (
        easy_questions[:easy_q] +
        medium_questions[:medium_q] +
        hard_questions[:hard_q]
    )

    exam = []

    # Add DB questions to exam
    for q in selected_questions:
        exam.append({
            "id": q.id,
            "subject": q.subject,
            "topic": q.topic,
            "difficulty": q.difficulty,
            "question": decrypt(q.encrypted_content)
        })

    # If DB questions are not enough → generate AI questions
    while len(exam) < num_questions:

        generated = generate_coulomb_question()

        exam.append({
            "id": "AI_GENERATED",
            "subject": generated["subject"],
            "topic": generated["topic"],
            "difficulty": generated["difficulty"],
            "question": generated["question"]
        })

    # Shuffle final exam
    random.shuffle(exam)

    return {
        "blueprint": blueprint,
        "total_questions": len(exam),
        "questions": exam
    }
# ---------------------------------
# Activity Monitoring API
# ---------------------------------

@router.post("/activity")
def track_activity(tab_switches: int, fullscreen_exit: int, copy_attempts: int):

    risk = calculate_risk(tab_switches, fullscreen_exit, copy_attempts)

    return {
        "risk_score": risk["risk_score"],
        "status": risk["status"]
    }
@router.post("/submit")
def submit_exam(responses: list):

    result = calculate_result(responses)

    feedback = generate_feedback(result)

    return {
        "score": result["score"],
        "accuracy": result["accuracy"],
        "weak_topics": result["weak_topics"],
        "strong_topics": result["strong_topics"],
        "feedback": feedback
    }
@router.post("/start")
def start_exam(user_email: str, subject: str):

    db = SessionLocal()

    session = ExamSession(
        user_email=user_email,
        subject=subject,
        status="ACTIVE"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "message": "Exam session started",
        "session_id": session.id
    }
@router.post("/answer")

def save_answer(session_id: int, question_id: int, answer: str):

    return {
        "session_id": session_id,
        "question_id": question_id,
        "answer": answer,
        "status": "saved"
    }

@router.post("/end")
def end_exam(session_id: int):

    db = SessionLocal()

    session = db.query(ExamSession).filter(
        ExamSession.id == session_id
    ).first()

    if not session:
        return {"error": "Session not found"}

    session.status = "COMPLETED"

    db.commit()

    return {
        "message": "Exam finished successfully"
    }