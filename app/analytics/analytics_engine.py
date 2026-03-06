def calculate_result(responses):

    total_questions = len(responses)
    correct_answers = 0

    topic_stats = {}

    for r in responses:

        topic = r["topic"]

        if topic not in topic_stats:
            topic_stats[topic] = {
                "correct": 0,
                "total": 0
            }

        topic_stats[topic]["total"] += 1

        if r["is_correct"]:
            correct_answers += 1
            topic_stats[topic]["correct"] += 1

    accuracy = (correct_answers / total_questions) * 100

    weak_topics = []
    strong_topics = []

    for topic, stats in topic_stats.items():

        topic_accuracy = (stats["correct"] / stats["total"]) * 100

        if topic_accuracy < 50:
            weak_topics.append(topic)

        else:
            strong_topics.append(topic)

    return {
        "score": correct_answers,
        "accuracy": accuracy,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics
    }