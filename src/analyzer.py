import os
import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:


    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found:\n{file_path}")

    name_nd_ext = os.path.splitext(file_path)
    extension = name_nd_ext[1].lower()

    if extension == ".csv":
        return pd.read_csv(file_path)

    elif extension == ".xlsx":
        return pd.read_excel(file_path)

    else:
        raise ValueError(
            "Only CSV and Excel files are supported."
        )


def validate_data(df: pd.DataFrame):
    

    errors = []
    warnings = []

    #emoty file
    if df.empty:
        errors.append("The uploaded file is empty.")
        return errors, warnings

    #Columns required
    required = [
        "Student_ID",
        "Name"
    ]

    for column in required:

        if column not in df.columns:
            errors.append(
                f"Missing required column: {column}"
            )

    if errors:
        return errors, warnings


    if df["Student_ID"].isnull().any():
        errors.append(
            "Some Student IDs are missing."
        )

    if df["Name"].isnull().any():
        errors.append(
            "Some student names are missing."
        )

    duplicates = df[df["Student_ID"].duplicated()]

    if not duplicates.empty:

        ids = duplicates["Student_ID"].tolist()

        errors.append(
            f"Duplicate Student IDs found: {ids}"
        )

    excluded = [
        "Student_ID",
        "Name",
        "Average",
        "Grade",
        "Result"
    ]

    subjects = []

    for column in df.columns:

        if column not in excluded:
            subjects.append(column)

    for subject in subjects:

        marks = pd.to_numeric(
            df[subject],
            errors="coerce"
        )

        if df[subject].isnull().any():
            warnings.append(
                f"{subject}: Missing marks."
            )

        invalid = marks.isnull() & df[subject].notnull()
        if invalid.any():

            warnings.append(
                f"{subject}: Non-numeric values."
            )

        if (marks < 0).any():

            warnings.append(
                f"{subject}: Negative marks found."
            )

        if (marks > 100).any():

            warnings.append(
                f"{subject}: Marks above 100 found."
            )

    return errors, warnings




def calculate_student_averages(df) -> pd.DataFrame:

    excluded = [
        "Student_ID",
        "Name",
        "Average",
        "Grade",
        "Result"
    ]
    subjects = []

    for column in df.columns:

        if column not in excluded:
            subjects.append(column)

    marks = df[subjects].apply(
        pd.to_numeric,
        errors="coerce"
    )

    df["Average"] = marks.mean(axis=1).round(2)

    return df


def assign_grades(df: pd.DataFrame) -> pd.DataFrame:

    grades = []
    for average in df["Average"]:

        if average >= 95:
            grades.append("A+")

        elif average >= 90:
            grades.append("A")

        elif average >= 85:
            grades.append("B+")

        elif average >= 80:
            grades.append("B")

        elif average >= 70:
            grades.append("C+")

        elif average >= 60:
            grades.append("C")

        elif average >= 50:
            grades.append("D")

        else:
            grades.append("F")

    df["Grade"] = grades

    return df



def determine_pass_fail(df: pd.DataFrame)-> pd.DataFrame:

    results = []
    for grade in df["Grade"]:

        if grade == "F":

            results.append("Fail")

        elif grade in ["A", "A+"]:

            results.append("Distinction")

        else:

            results.append("Passed")

    df["Result"] = results

    return df


def calculate_class_statistics(df: pd.DataFrame):

    total = len(df)

    passed = len(df[df["Result"] != "Fail"])

    failed = len(
        df[df["Result"] == "Fail"]
    )

    distinctions = len(
        df[df["Result"] == "Distinction"]
    )

    statistics = {
        "Number of Students": total,

        "Class Average": round(df["Average"].mean(), 2),

        "Highest Average":round(df["Average"].max(), 2),

        "Lowest Average":round(df["Average"].min(), 2),

        "Median Average": round(df["Average"].median(), 2),

        "Standard Deviation":round(df["Average"].std(), 2),

        "Students Passed": passed,

        "Students Failed":failed,

        "Pass Rate (%)": round((passed / total) * 100, 2),

        "Fail Rate (%)": round((failed / total) * 100, 2),

        "Distinction Rate (%)": round((distinctions / total) * 100, 2)

    }

    return statistics


def get_top_students(df,number = 5):

    return (
        df.sort_values(
            by="Average",
            ascending=False
        )
        .head(number)
    )



def get_at_risk_students(df: pd.DataFrame):

    return df[df["Average"] < 50]