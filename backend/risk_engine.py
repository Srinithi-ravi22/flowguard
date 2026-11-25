
# =========================================
# FLOWGUARD RISK ENGINE
# =========================================

def calculate_risk_breakdown(
    repetitions,
    no_state_change_count,
    executions,
    loop_detected
):
    # 1. Repetition risk (maximum 25)
    repetition_risk = min(repetitions * 5, 25)

    # 2. Loop detection risk (maximum 25)
    loop_risk = 25 if loop_detected else 0

    # 3. No state change risk (maximum 20)
    state_change_risk = min(no_state_change_count * 2, 20)

    # 4. Execution volume risk (maximum 20)
    if executions > 50:
        execution_risk = 20
    elif executions > 20:
        execution_risk = 10
    elif executions > 10:
        execution_risk = 5
    else:
        execution_risk = 0

    total_risk = min(
        repetition_risk + loop_risk + state_change_risk + execution_risk,
        100
    )

    return {
        "repetition_risk": repetition_risk,
        "loop_risk": loop_risk,
        "state_change_risk": state_change_risk,
        "execution_risk": execution_risk,
        "total_score": total_risk
    }


# =========================================
# RISK SCORE
# =========================================

def calculate_risk(
    repetitions,
    no_state_change_count,
    executions,
    loop_detected
):
    breakdown = calculate_risk_breakdown(
        repetitions,
        no_state_change_count,
        executions,
        loop_detected
    )

    return breakdown["total_score"]


# =========================================
# SEVERITY CLASSIFICATION
# =========================================

def get_severity(risk_score):

    if risk_score >= 80:
        return "CRITICAL"

    elif risk_score >= 60:
        return "HIGH"

    elif risk_score >= 30:
        return "MEDIUM"

    else:
        return "LOW"
