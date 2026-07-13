import os
import matplotlib.pyplot as plt
import pandas as pd

def grade_plot(df):

    #Count how many students received each grade
    _grade_value_counts = df['Grade'].value_counts()
    count_grade = _grade_value_counts.sort_index()

    #create the figure
    plt.figure(figsize=(8,5))

    #draw the bar char
    plt.bar(count_grade.index,count_grade.values)

    # Add chart labels
    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")

    # Display horizontal grid lines
    plt.grid(axis="y")

    # Save the chart as a PNG image
    plt.savefig("graphs/grade_distribution.png")

    plt.close()

def pie_plot(df):

    # Count the number of students are in each result category
    result_counts = df["Result"].value_counts()
    # Create the figure
    plt.figure(figsize=(7, 7))
    # Draw the pie chart
    plt.pie(
        result_counts.values,
        labels=result_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    # Add a title
    plt.title("Pass/Fail Distribution")
    # Make the pie chart circular
    plt.axis("equal")
    # Save the graphs
    plt.savefig("graphs/pass_fail_pie.png")
    # Close the figure
    plt.close()

def plot_module_averages(df):

    excluded = [
        "Student_ID",
        "Name",
        "Average",
        "Grade",
        "Result"
    ]

    subject_columns = []

    for col in df.columns:
        if col not in excluded:
            subject_columns.append(col)

    subject_averages = (
        df[subject_columns]
        .apply(pd.to_numeric, errors="coerce")
        .mean()
    )

    plt.figure(figsize=(8,5))

    plt.bar(
        subject_averages.index,
        subject_averages.values
    )

    plt.title("Average Marks Per Module")
    plt.xlabel("Module")
    plt.ylabel("Average")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.savefig("graphs/module_averages.png")

    plt.close()