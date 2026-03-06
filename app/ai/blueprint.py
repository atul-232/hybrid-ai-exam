def generate_blueprint(total_questions: int):

    easy = int(total_questions * 0.3)
    medium = int(total_questions * 0.5)
    hard = total_questions - (easy + medium)

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard
    }