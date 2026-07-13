# Student Grade Analyzer

A professional Python application that analyzes student performance from CSV and Excel datasets.

The application validates uploaded data, calculates student averages, assigns grades, determines pass/fail status, generates summary statistics, and displays an interactive dashboard built with Streamlit.

---

# Features

## Data Import

- Read CSV files
- Read Excel (.xlsx) files

---

## Data Validation
The application automatically checks for:
- Missing Student IDs
- Missing student names
- Duplicate Student IDs
- Missing marks
- Non-numeric marks
- Marks below 0
- Marks above 100

Validation issues are classified as:
- *Errors* – stop the analysis
- *Warnings* – displayed while allowing analysis to continue

---

## Student Analysis
The application automatically calculates:

- Student averages
- Letter grades
- Pass/Fail status
- Distinctions


## Class Statistics
The dashboard displays:

- Number of students
- Class average
- Highest average
- Lowest average
- Median average
- Standard deviation
- Pass rate
- Fail rate
- Distinction rate

---

## Dashboard
The Streamlit dashboard provides:

- Dataset upload
- Validation messages
- Dashboard metrics
- Student results table
- Grade distribution chart
- Pass/Fail chart
- Subject average chart
- Top-performing students
- At-risk students
- Download processed dataset

---

# Technologies Used
- Python 3
- Pandas
- NumPy
- Matplotlib
- Streamlit
- OpenPyXL

---

# Installation

Clone the repository.

`bash
git clone https://github.com/Masenya-JNK-tech/StudentGradeAnalyzer.git


## Move into the project.

```bash
cd StudentGradeAnalyzer
```

### Install the dependencies.
`bash
pip install -r requirements.txt
---

# Running the Application

## Streamlit Dashboard

- bash
streamlit run dashboard.py

---

## Command Line Version

-bash
python main.py

---

# Example Workflow
1. Upload a CSV or Excel dataset.
2. The application validates the data.
3. Student averages are calculated.
4. Grades are assigned.
5. Pass/Fail status is determined.
6. Charts and tables are displayed.
7. Download the processed dataset.
