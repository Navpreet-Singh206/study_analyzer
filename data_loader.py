from pathlib import Path
import pandas as pd
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "study_log.csv"
SUBJECTS = ["Maths", "Physics", "Python", "English"]
TIMES_OF_DAY = ["Morning", "Afternoon", "Evening", "Night"]
REQUIRED_COLUMNS = ["date", "subject", "study_hours", "time_of_day", "marks"]


def get_csv_path():
    return CSV_PATH


def load_data(csv_path=None):
    path = Path(csv_path) if csv_path else CSV_PATH
    if not path.exists():
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    df = pd.read_csv(path)
    return df


def clean_data(df):
    df = df.copy()
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[REQUIRED_COLUMNS]
    df = df.dropna(how="all")

   
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

   
    df["study_hours"] = pd.to_numeric(df["study_hours"], errors="coerce")
    df["marks"] = pd.to_numeric(df["marks"], errors="coerce")

    # Tidy text columns: strip spaces and use a consistent spelling.
    df["subject"] = df["subject"].astype(str).str.strip().str.title()
    df["time_of_day"] = df["time_of_day"].astype(str).str.strip().str.title()

    # Replace "Nan" that can appear after converting missing text to string.
    df.loc[df["subject"].isin(["Nan", "None", ""]), "subject"] = pd.NA
    df.loc[df["time_of_day"].isin(["Nan", "None", ""]), "time_of_day"] = pd.NA

    # Drop rows that are still missing a required value.
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # Keep only sensible ranges (hours and exam-style marks).
    df = df[(df["study_hours"] >= 0) & (df["study_hours"] <= 24)]
    df = df[(df["marks"] >= 0) & (df["marks"] <= 100)]

    # Add weekday, for example "Monday", using Pandas datetime methods.
    df["weekday"] = df["date"].dt.day_name()

    # Sort oldest to newest so the line chart reads left-to-right in time.
    df = df.sort_values("date").reset_index(drop=True)

    return df


def load_clean_data(csv_path=None):
   
    raw = load_data(csv_path)
    return clean_data(raw)


def average_marks_by_subject(df):

    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("subject", as_index=True)["marks"].mean()


def average_marks_by_time_of_day(df):
    if df.empty:
        return pd.Series(dtype=float)

    averages = df.groupby("time_of_day", as_index=True)["marks"].mean()
    ordered = [t for t in TIMES_OF_DAY if t in averages.index]
    return averages.reindex(ordered)


def append_entry(date, subject, study_hours, time_of_day, marks, csv_path=None):
    
    path = Path(csv_path) if csv_path else CSV_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    new_row = pd.DataFrame(
        [
            {
                "date": pd.to_datetime(date).strftime("%Y-%m-%d"),
                "subject": subject,
                "study_hours": float(study_hours),
                "time_of_day": time_of_day,
                "marks": float(marks),
            }
        ]
    )

    write_header = (not path.exists()) or path.stat().st_size == 0
    new_row.to_csv(path, mode="a", header=write_header, index=False)
    return new_row
