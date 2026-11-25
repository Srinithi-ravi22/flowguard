
# =========================================
# FLOWGUARD RECOMMENDATION ENGINE
# =========================================

def generate_root_cause(
    loop_result,
    no_state_change_count,
    executions
):

    if loop_result["loop_detected"] and no_state_change_count > 0:

        pattern = " -> ".join(loop_result["pattern"])

        return (
            f"Repeating event cycle detected: {pattern}. "
            "Repeated executions are occurring without "
            "meaningful state changes."
        )

    elif loop_result["loop_detected"]:

        pattern = " -> ".join(loop_result["pattern"])

        return (
            f"Repeated event sequence detected: {pattern}. "
            "This may indicate a workflow trigger cycle."
        )

    elif no_state_change_count > 0:

        return (
            "Repeated actions were detected without "
            "meaningful state changes."
        )

    elif executions > 50:

        return (
            "High execution volume detected. "
            "The workflow may be triggering too frequently."
        )

    return "No major abnormal behavior identified in the supplied data."


# =========================================
# PREVENTION RECOMMENDATIONS
# =========================================

def generate_recommendation(
    loop_detected,
    no_state_change_count,
    executions
):

    if loop_detected and no_state_change_count > 0:

        return (
            "Enable duplicate-event protection, verify state changes "
            "before triggering actions, and add a cooldown."
        )

    elif loop_detected:

        return (
            "Add a loop guard, execution limit, and cooldown "
            "to prevent repeated workflow triggers."
        )

    elif no_state_change_count > 0:

        return (
            "Skip actions when the system state has not changed. "
            "Add a no-state-change guard."
        )

    elif executions > 50:

        return (
            "Review trigger frequency and apply rate limiting "
            "or execution thresholds."
        )

    return (
        "Workflow appears normal. Continue monitoring "
        "for unexpected event patterns."
    )
