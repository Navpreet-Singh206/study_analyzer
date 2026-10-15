import streamlit as st

from analysis import build_insights, predict_marks, summarise, trend_line_points
from charts import plot_hours_vs_marks, plot_marks_by_time_of_day, plot_marks_over_time
from data_loader import (
    SUBJECTS,
    TIMES_OF_DAY,
    append_entry,
    average_marks_by_subject,
    average_marks_by_time_of_day,
    load_clean_data,
)


def configure_page():
    st.set_page_config(page_title="Study Habits Analyzer", layout="wide")


def render_sidebar_form():
    st.sidebar.header("Add a study session")
    st.sidebar.caption("New rows are appended to data/study_log.csv")

    with st.sidebar.form("new_entry"):
        date = st.date_input("Date")
        subject = st.selectbox("Subject", SUBJECTS)
        hours = st.number_input(
            "Study hours",
            min_value=0.0,
            max_value=24.0,
            value=2.0,
            step=0.5,
        )
        time_of_day = st.selectbox("Time of day", TIMES_OF_DAY)
        marks = st.number_input(
            "Marks",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=1.0,
        )
        submitted = st.form_submit_button("Save entry")

    if submitted:
        append_entry(date, subject, hours, time_of_day, marks)
        st.sidebar.success("Saved to study_log.csv")
        # Reload so the new row appears in charts immediately.
        st.rerun()


def render_metrics(stats):
    col1, col2, col3 = st.columns(3)
    col1.metric("Average study hours", _fmt(stats["avg_hours"], 2))
    col2.metric("Average marks", _fmt(stats["avg_marks"], 1))
    col3.metric("Hours vs marks (r)", _fmt(stats["correlation"], 2))


def render_warning(count):
   
    if count < 10:
        st.warning(
            "Fewer than 10 entries: these charts show a trend only, not proof "
            "that study hours cause better marks."
        )


def render_insights(insights):
    st.subheader("Insights")
    for line in insights:
        st.write(f"- {line}")


def render_predictor(stats):
    st.subheader("Marks predictor")
    st.caption("Uses a straight-line model fitted with NumPy polyfit (marks ≈ slope × hours + intercept).")

    hours = st.number_input(
        "If I study this many hours…",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.5,
        key="predict_hours",
    )

    if stats["coeffs"] is None:
        st.info("Need at least two sessions before a prediction can be made.")
        return

    expected = predict_marks(hours, stats["coeffs"])
    st.success(f"Expected marks: **{expected:.1f}** (trend only, not a guarantee).")
    st.caption(
        f"Line equation: marks ≈ {stats['slope']:.2f} × hours + {stats['intercept']:.2f}"
    )


def render_tables(df, by_subject, by_time):

    st.subheader("Your study log")
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.caption("Average marks by subject (Pandas group-by)")
        st.dataframe(by_subject.rename("average_marks"), use_container_width=True)
    with col2:
        st.caption("Average marks by time of day (Pandas group-by)")
        st.dataframe(by_time.rename("average_marks"), use_container_width=True)


def _fmt(value, digits):
    try:
        if value != value:  # NaN check
            return "—"
        return f"{value:.{digits}f}"
    except (TypeError, ValueError):
        return "—"


def main():
    configure_page()
    st.title("Study Habits Analyzer")
    st.write(
        "Log study hours, time of day, and marks. The app checks whether more "
        "hours go with better marks, and which time of day works best."
    )

    render_sidebar_form()

    df = load_clean_data()
    stats = summarise(df)
    by_subject = average_marks_by_subject(df)
    by_time = average_marks_by_time_of_day(df)
    insights = build_insights(df, stats, by_time)

    render_warning(stats["count"])
    render_metrics(stats)
    render_insights(insights)

    x_line, y_line = trend_line_points(df["study_hours"] if not df.empty else [], stats["coeffs"])

    st.subheader("Charts")
    c1, c2 = st.columns(2)
    with c1:
        st.pyplot(plot_hours_vs_marks(df, x_line, y_line), clear_figure=True)
    with c2:
        st.pyplot(plot_marks_by_time_of_day(by_time), clear_figure=True)

    st.pyplot(plot_marks_over_time(df), clear_figure=True)

    render_predictor(stats)
    render_tables(df, by_subject, by_time)


if __name__ == "__main__":
    main()
