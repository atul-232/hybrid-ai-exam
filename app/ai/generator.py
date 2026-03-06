import random

def generate_coulomb_question():

    k = 9 * 10**9

    q1 = random.randint(1,5) * 1e-6
    q2 = random.randint(1,5) * 1e-6
    r = random.randint(1,5)

    force = k * q1 * q2 / (r**2)

    question = f"""
Two charges {q1} C and {q2} C are placed {r} m apart.
Find the electrostatic force between them.
"""

    return {
        "subject": "Physics",
        "topic": "Electrostatics",
        "difficulty": 2,
        "question": question,
        "answer": force
    }