'''
This module retrieves computer science course information from the UNSW
Timetable website,parses the data, and creates a CSV file with course codes,
names, and types (undergraduate or postgraduate).

This script was used over webscrape.py as it only scraped course names
of T3 2023 COMP courses.
'''

import subprocess
import re
import pandas as pd
import sys


def get_courses_code_and_name(url):
    """
    Retrieves and processes computer science course codes and names from the UNSW
    Timetable website.

    Parameters:
    - url (str): The URL of the UNSW Timetable website for computer science courses.

    Returns:
    - list: A list of formatted course strings containing course codes and names.
    """
    proc = subprocess.run(
        ["curl", "--location", "--silent", url], capture_output=True, text=True
    )

    courses = []
    all_courses = []

    for m in re.findall(
        rf"^.*COMP[0-9]{{4}}\.html.*$", proc.stdout, flags=re.MULTILINE
    ):
        m = re.search(
            r"""<a href="(?P<code>[A-Z]{4}[0-9]{4})\.html">(?P<name>.*?)</a>""", m
        )
        code = m.group("code")
        name = m.group("name")
        if code != name:
            courses.append((code, name))

    for code, name in sorted(set(courses)):
        all_courses.append(f"{code} {name}")

    return all_courses


undergrad = f"https://timetable.unsw.edu.au/2023/KENSUGRDT3COMP.html"
postgrad = f"https://timetable.unsw.edu.au/2023/KENSPGRDT3COMP.html"

undergrad_courses = get_courses_code_and_name(undergrad)
postgrad_courses = get_courses_code_and_name(postgrad)

# Separate course name and course code into separate fields of the dataframe
udrg_courses = [
    {"Course Code": course.split()[0], "Course Name": " ".join(course.split()[1:])}
    for course in undergrad_courses
]
pgrd_courses = [
    {"Course Code": course.split()[0], "Course Name": " ".join(course.split()[1:])}
    for course in postgrad_courses
]


for course in udrg_courses:
    course["Type"] = "undergraduate"

for course in pgrd_courses:
    course["Type"] = "postgraduate"

df_udrg = pd.DataFrame(udrg_courses)
df_pgrd = pd.DataFrame(pgrd_courses)


combined_df = pd.concat([df_udrg, df_pgrd], ignore_index=True)
combined_df.to_csv("comp_courses.csv", index=False, line_terminator="\n")
