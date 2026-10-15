# Study Habits Analyzer

A beginner-friendly Python assignment that uses **Pandas**, **NumPy**, **Matplotlib**, and **Streamlit**.

You log study hours, time of day, and marks. The app shows:

- whether more study hours tend to go with higher marks
- which time of day has the best average marks
- a simple prediction of marks from study hours

## Project structure

```
study_analyzer/
├── data/study_log.csv   # sample log (20 rows)
├── data_loader.py       # Pandas: load, clean, group-by, append
├── analysis.py          # NumPy: mean, std, correlation, polyfit
├── charts.py            # Matplotlib: scatter, bar, line
├── app.py               # Streamlit frontend
└── requirements.txt
```

## How to run

1. Open a terminal and go to this folder:

   ```bash
   cd study_analyzer
   ```

2. Create a virtual environment (recommended) and install libraries:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   On Windows (Command Prompt):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Start the app:

   ```bash
   streamlit run app.py
   ```

4. Your browser should open the dashboard. Use the **sidebar** to add a new study session.

Python 3.9 or newer is required.

## How the files work

**`data/study_log.csv`**  
CSV columns: `date`, `subject`, `study_hours`, `time_of_day`, `marks`.  
Example: `2026-09-20, Maths, 2.5, Night, 72`.

**`data_loader.py` (Pandas)**  
Reads the CSV, converts dates, drops missing values, adds a `weekday` column, groups average marks by subject and by time of day, and appends new rows from the form.

**`analysis.py` (NumPy)**  
`np.mean` and `np.std` for averages and consistency, `np.corrcoef` for hours vs marks, `np.polyfit` / `np.polyval` for the trend line and the marks predictor.

**`charts.py` (Matplotlib)**  
(1) scatter of hours vs marks with a trend line, (2) bar chart of average marks by time of day, (3) line chart of marks over dates. Each chart has a title, axis labels, and a legend where needed.

**`app.py` (Streamlit)**  
Browser UI: sidebar form, metric cards, charts, auto insights, hours-to-marks predictor, and a warning if there are fewer than 10 entries.

## Viva questions

**1. Why do we use Pandas instead of reading the CSV with plain Python?**  
Pandas loads the table into a DataFrame, converts types, handles missing values, and supports `groupby` in a few lines. That is faster and clearer than looping over rows by hand.

**2. What does the correlation value `r` mean?**  
`np.corrcoef` gives Pearson’s r between study hours and marks. Close to +1 means more hours tend to go with higher marks; close to 0 means little linear link. Correlation is not proof of cause.

**3. How does the marks predictor work?**  
`np.polyfit` fits a straight line `marks ≈ slope × hours + intercept`. `np.polyval` then estimates marks for the hours you type. It is a trend from past data, not a guarantee.

**4. Why might Morning look “best” on the bar chart?**  
The bar chart shows **average marks** for each time of day (Pandas `groupby`). If Morning has the highest average in *this* log, the insight reports that. A larger or different log could change the result.

**5. Why does the app warn you when there are fewer than 10 entries?**  
A small sample can look like a strong pattern by chance. The warning reminds you that the charts are a **trend**, not scientific proof that extra hours cause better marks.
