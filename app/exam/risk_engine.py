def calculate_risk(tab_switches: int, fullscreen_exit: int, copy_attempts: int):

    risk_score = 0

    risk_score += tab_switches * 25
    risk_score += fullscreen_exit * 20
    risk_score += copy_attempts * 30

    if risk_score >= 70:
        return {
            "risk_score": risk_score,
            "status": "AUTO_SUBMIT"
        }

    elif risk_score >= 40:
        return {
            "risk_score": risk_score,
            "status": "WARNING"
        }

    else:
        return {
            "risk_score": risk_score,
            "status": "SAFE"
        }