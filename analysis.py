import numpy as np


def _to_array(values):
    return np.array(values, dtype=float)


def average_and_consistency(values):
    arr = _to_array(values)
    if arr.size == 0:
        return np.nan, np.nan
    return float(np.mean(arr)), float(np.std(arr))


def hours_marks_correlation(hours, marks):
    x = _to_array(hours)
    y = _to_array(marks)

    # Need at least 2 points, and both arrays must vary a little.
    if x.size < 2 or y.size < 2:
        return np.nan
    if np.std(x) == 0 or np.std(y) == 0:
        return np.nan

    matrix = np.corrcoef(x, y)
    return float(matrix[0, 1])


def fit_hours_marks_trend(hours, marks, degree=1):

    x = _to_array(hours)
    y = _to_array(marks)

    if x.size < 2:
        return None, np.nan, np.nan

    coeffs = np.polyfit(x, y, deg=degree)
    # For a line, coeffs[0] is slope and coeffs[1] is intercept.
    slope = float(coeffs[0])
    intercept = float(coeffs[1]) if len(coeffs) > 1 else 0.0
    return coeffs, slope, intercept


def predict_marks(hours_input, coeffs):
    
    if coeffs is None:
        return np.nan
    predicted = float(np.polyval(coeffs, hours_input))
    return float(np.clip(predicted, 0, 100))


def trend_line_points(hours, coeffs, num_points=50):
    x = _to_array(hours)
    if coeffs is None or x.size == 0:
        return np.array([]), np.array([])

    x_line = np.linspace(float(np.min(x)), float(np.max(x)), num_points)
    y_line = np.polyval(coeffs, x_line)
    return x_line, y_line


def summarise(df):
    hours = df["study_hours"] if not df.empty else []
    marks = df["marks"] if not df.empty else []

    avg_hours, std_hours = average_and_consistency(hours)
    avg_marks, std_marks = average_and_consistency(marks)
    r = hours_marks_correlation(hours, marks)
    coeffs, slope, intercept = fit_hours_marks_trend(hours, marks)

    return {
        "count": int(len(df)),
        "avg_hours": avg_hours,
        "std_hours": std_hours,
        "avg_marks": avg_marks,
        "std_marks": std_marks,
        "correlation": r,
        "coeffs": coeffs,
        "slope": slope,
        "intercept": intercept,
    }


def build_insights(df, stats, marks_by_time):
    insights = []

    if stats["count"] == 0:
        return ["No study entries yet. Add a session from the sidebar to begin."]

    # Best time of day (highest average marks).
    if marks_by_time is not None and len(marks_by_time) > 0:
        best_time = marks_by_time.idxmax()
        best_avg = float(marks_by_time.max())
        insights.append(
            f"Your best marks come from {best_time} study (avg {best_avg:.0f})."
        )

    # Hours vs marks relationship.
    r = stats["correlation"]
    if np.isnan(r):
        insights.append("Not enough variation yet to measure hours vs marks.")
    elif r >= 0.3:
        insights.append(
            f"More study hours are linked to higher marks (r = {r:.2f})."
        )
    elif r <= -0.3:
        insights.append(
            f"More study hours are linked to lower marks (r = {r:.2f}). "
            "Quality of study may matter more than extra hours."
        )
    else:
        insights.append(
            f"Study hours and marks show a weak linear link (r = {r:.2f})."
        )

    # Consistency of marks.
    if not np.isnan(stats["std_marks"]):
        insights.append(
            f"Marks consistency (standard deviation) is {stats['std_marks']:.1f} "
            "(lower means more consistent scores)."
        )

    return insights
