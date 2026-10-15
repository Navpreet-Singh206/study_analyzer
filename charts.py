import matplotlib.pyplot as plt
import numpy as np

def _style_axes(ax, title, xlabel, ylabel):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.4)

def plot_hours_vs_marks(df, x_line, y_line):
    fig, ax = plt.subplots(figsize=(7, 4))

    if df.empty:
        ax.text(0.5, 0.5, "No data to plot", ha="center", va="center")
        _style_axes(ax, "Study Hours vs Marks", "Study hours", "Marks")
        fig.tight_layout()
        return fig

    ax.scatter(
        df["study_hours"],
        df["marks"],
        label="Study sessions",
        color="#2563eb",
        alpha=0.8,
    )
    if x_line is not None and len(x_line) > 0:
        ax.plot(
            x_line,
            y_line,
            color="#dc2626",
            linewidth=2,
            label="Trend line (NumPy polyfit)",
        )

    ax.legend()
    _style_axes(ax, "Study Hours vs Marks", "Study hours", "Marks")
    fig.tight_layout()
    return fig


def plot_marks_by_time_of_day(marks_by_time):
    
    fig, ax = plt.subplots(figsize=(7, 4))

    if marks_by_time is None or len(marks_by_time) == 0:
        ax.text(0.5, 0.5, "No data to plot", ha="center", va="center")
        _style_axes(ax, "Average Marks by Time of Day", "Time of day", "Average marks")
        fig.tight_layout()
        return fig

    times = list(marks_by_time.index)
    averages = np.array(marks_by_time.values, dtype=float)
    bars = ax.bar(times, averages, color="#0d9488", label="Average marks")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.set_ylim(0, 100)
    ax.legend()
    _style_axes(ax, "Average Marks by Time of Day", "Time of day", "Average marks")
    fig.tight_layout()
    return fig


def plot_marks_over_time(df):
    fig, ax = plt.subplots(figsize=(7, 4))

    if df.empty:
        ax.text(0.5, 0.5, "No data to plot", ha="center", va="center")
        _style_axes(ax, "Marks Over Time", "Date", "Marks")
        fig.tight_layout()
        return fig
    ax.plot(
        df["date"],
        df["marks"],
        marker="o",
        color="#7c3aed",
        label="Marks",
    )
    ax.legend()
    _style_axes(ax, "Marks Over Time", "Date", "Marks")
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig
