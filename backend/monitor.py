
from collections import Counter


def detect_loop(events):
    """
    Detect a repeating sequence at the end of an event stream.

    Example:
    A, B, A, B, A, B -> pattern A, B repeated 3 times.
    """

    event_names = [event["event"] for event in events]
    n = len(event_names)

    best_pattern = []
    best_repetitions = 1

    # Check possible pattern lengths
    for pattern_length in range(1, n // 2 + 1):

        pattern = event_names[-pattern_length:]

        repetitions = 1
        position = n - pattern_length

        # Count consecutive matching patterns backwards
        while position - pattern_length >= 0:

            previous_pattern = event_names[
                position - pattern_length:position
            ]

            if previous_pattern == pattern:
                repetitions += 1
                position -= pattern_length
            else:
                break

        if repetitions >= 2:

            if (
                repetitions > best_repetitions
                or (
                    repetitions == best_repetitions
                    and len(pattern) > len(best_pattern)
                )
            ):
                best_pattern = pattern
                best_repetitions = repetitions

    # Count individual event occurrences
    counts = Counter(event_names)

    repeated_events = {
        event: count
        for event, count in counts.items()
        if count > 1
    }

    return {
        "total_events": n,
        "loop_detected": best_repetitions >= 2,
        "pattern": best_pattern,
        "repetitions": best_repetitions,
        "repeated_events": repeated_events,
    }


def calculate_risk(analysis, baseline=None):
    """
    Calculate workflow risk based on repetition patterns,
    configured baseline, and event volume.
    """

    score = 0
    breakdown = {}

    # Default baseline if a workflow has no configuration
    if baseline is None:
        baseline = {
            "expected_events": 2,
            "max_repetitions": 1,
            "allowed_retries": 0
        }

    expected_events = baseline["expected_events"]
    max_repetitions = baseline["max_repetitions"]
    allowed_retries = baseline["allowed_retries"]

    # Calculate permitted repetition limit
    repetition_limit = max_repetitions + allowed_retries

    # Calculate repetitions beyond the permitted limit
    excess_repetitions = max(
        0,
        analysis["repetitions"] - repetition_limit
    )

    # 1. Loop Risk
    if excess_repetitions > 0:
        breakdown["loop_risk"] = 40
        score += 40
    else:
        breakdown["loop_risk"] = 0

    # 2. Excess Repetition Risk
    repetition_risk = min(
        max(excess_repetitions - 1, 0) * 10,
        30
    )

    breakdown["repetition_risk"] = repetition_risk
    score += repetition_risk

    # 3. Duplicate Event Risk
    if excess_repetitions > 0 and analysis["repeated_events"]:
        breakdown["duplicate_event_risk"] = 10
        score += 10
    else:
        breakdown["duplicate_event_risk"] = 0

    # 4. Event Volume Risk
    expected_volume = (
        expected_events * max(max_repetitions, 1) * 3
    )

    if analysis["total_events"] >= max(20, expected_volume):
        breakdown["event_volume_risk"] = 20
        score += 20
    else:
        breakdown["event_volume_risk"] = 0

    # Ensure score never exceeds 100
    score = min(score, 100)

    # Determine severity
    if score >= 80:
        severity = "CRITICAL"
    elif score >= 60:
        severity = "HIGH"
    elif score >= 30:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "risk_score": score,
        "severity": severity,
        "risk_breakdown": breakdown,
        "alert": score >= 60
    }
