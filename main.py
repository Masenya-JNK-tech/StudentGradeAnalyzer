import os
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from src.analyzer import*

from src.visualizer import (
    grade_plot,
    pie_plot,
    plot_module_averages
)


def main():

    # Hide the Tkinter root window
    Tk().withdraw()

    # Choose file
    file_path = askopenfilename(
        title="Select Student Dataset",
        filetypes=[
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx")
        ]
    )

    if not file_path:
        print("No file selected.")
        return

    # Load data
    students = load_data(file_path)

    # Validate data
    errors, warnings = validate_data(students)

    if errors:
        print("\n===== VALIDATION ERRORS =====")

        for error in errors:
            print(f"• {error}")

        return

    if warnings:
        print("\n===== VALIDATION WARNINGS =====")

        for warning in warnings:
            print(f"• {warning}")

    else:
        print("\nNo validation warnings found.")

    # Perform analysis
    students = calculate_student_averages(students)
    students = assign_grades(students)
    students = determine_pass_fail(students)

    # Class statistics
    stats = calculate_class_statistics(students)

    print("\n===== CLASS STATISTICS =====")

    for key, value in stats.items():
        print(f"{key}: {value}")

    # Create output folders if they don't exist

    # Generate graphs
    grade_plot(students)
    pie_plot(students)
    plot_module_averages(students)

    print("\nGraphs saved to the 'graphs' folder.")

    # Save processed dataset
    output_file = "reports/Student_Results.csv"
    students.to_csv(output_file, index=False)

    print(f"\nProcessed data saved to:\n{output_file}")

    # Top students
    print("\n===== TOP STUDENTS =====")
    print(get_top_students(students).reset_index(drop=True))

    # At-risk students
    print("\n===== AT-RISK STUDENTS =====")

    at_risk = get_at_risk_students(students)

    if at_risk.empty:
        print("No at-risk students.")
    else:
        print(at_risk.reset_index(drop=True))


if __name__ == "__main__":
    main()