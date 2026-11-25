
# =========================================
# FLOWGUARD RESOURCE WASTE CALCULATOR
# =========================================

def calculate_waste(
    executions,
    expected_executions,
    api_calls_per_execution,
    execution_time_ms
):

    # 1. Calculate excess executions
    excess_executions = max(
        0,
        executions - expected_executions
    )

    # 2. Calculate execution waste percentage
    if executions > 0:
        waste_percentage = (
            excess_executions / executions
        ) * 100
    else:
        waste_percentage = 0

    # 3. Calculate unnecessary API calls
    wasted_api_calls = (
        excess_executions * api_calls_per_execution
    )

    # 4. Calculate unnecessary execution time
    wasted_time_seconds = (
        excess_executions * execution_time_ms / 1000
    )

    # 5. Return all waste metrics
    return {
        "excess_executions": excess_executions,
        "estimated_wasted_api_calls": wasted_api_calls,
        "waste_percentage": round(waste_percentage, 2),
        "estimated_wasted_time_seconds": round(
            wasted_time_seconds, 2
        )
    }
