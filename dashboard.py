import streamlit as st
import pandas as pd

from src.analyzer import (validate_data,
    calculate_student_averages,
    assign_grades,
    determine_pass_fail,
    calculate_class_statistics,
    get_top_students,
    get_at_risk_students
)


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Student Grade Analyzer",
    page_icon="📊",
    layout="wide"
)

# HEADER

st.title("Student Grade Analyzer")
st.markdown(
    """
Analyze student performance from **CSV** and **Excel** files.

The application validates the uploaded data, calculates averages,
assigns grades, determines pass/fail status and displays useful
statistics and visualizations.
"""
)

# SIDEBAR

st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
Supported files:

• CSV (.csv)

• Excel (.xlsx)
"""
)


if uploaded_file is None:

    st.info("<<== Upload a student dataset from the sidebar.")

    st.stop()


# LOAD FILE

try:

    if uploaded_file.name.endswith(".csv"):

        students = pd.read_csv(uploaded_file)

    else:

        students = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(f"Unable to read file.\n\n{e}")

    st.stop()


# VALIDATE DATA
errors, warnings = validate_data(students)

if errors:

    st.error("❌ Critical Errors")

    for error in errors:

        st.write(f"• {error}")

    st.stop()

if warnings:
    st.warning("⚠ Validation Warnings")

    for warning in warnings:

        st.write(f"• {warning}")


# ANALYSIS
students = calculate_student_averages(students)

students = assign_grades(students)

students = determine_pass_fail(students)

statistics = calculate_class_statistics(students)

# ==========================================================
# DASHBOARD METRICS
# ==========================================================

st.header("Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Students",
    statistics["Number of Students"]
)

col2.metric(
    "Class Average",
    statistics["Class Average"]
)

col3.metric(
    "Pass Rate",
    f"{statistics['Pass Rate (%)']}%"
)

col4.metric(
    "Distinction Rate",
    f"{statistics['Distinction Rate (%)']}%"
)

st.divider()

# STUDENT TABLE
st.subheader("Student Results")

st.dataframe(
    students,
    use_container_width=True,
    hide_index=True
)

#Download Button

csv = students.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Results",
    data=csv,
    file_name="Student_Results.csv",
    mime="text/csv"
)

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("Grade Distribution")
    grade_counts = students["Grade"].value_counts().sort_index()
    st.bar_chart(grade_counts)

with right:

    st.subheader("Pass / Fail Distribution")

    result_counts = students["Result"].value_counts()

    st.bar_chart(result_counts)

st.divider()

# Subjects
st.subheader("Subject Averages")

excluded = [
    "Student_ID",
    "Name",
    "Average",
    "Grade",
    "Result"
]

subjects = [
    column
    for column in students.columns
    if column not in excluded
]

subject_average = students[subjects].mean()
st.bar_chart(subject_average)
st.divider()

## TOP STUDENTS
st.subheader("🏆 Top Students")

top_students = get_top_students(students)

st.dataframe(
    top_students,
    use_container_width=True,
    hide_index=True
)

#at risk students
st.subheader("⚠ At-Risk Students")
risk_students = get_at_risk_students(students)

if risk_students.empty:

    st.success("No at-risk students found.")

else:

    st.dataframe(
        risk_students,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.subheader("Class Statistics")

stats_df = pd.DataFrame(
    statistics.items(),
    columns=["Statistic", "Value"]
)

st.dataframe(
    stats_df,
    use_container_width=True,
    hide_index=True
)


st.caption(
    "Student Grade Analyzer | Built with Python, Pandas and Streamlit"
)