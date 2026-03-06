def generate_feedback(result):

    feedback = ""

    if result["accuracy"] >= 80:
        feedback += "Excellent performance. "

    elif result["accuracy"] >= 60:
        feedback += "Good performance but improvement needed. "

    else:
        feedback += "You need more practice. "

    if result["weak_topics"]:
        feedback += f"Weak areas: {', '.join(result['weak_topics'])}. "

    if result["strong_topics"]:
        feedback += f"Strong areas: {', '.join(result['strong_topics'])}. "

    return feedback