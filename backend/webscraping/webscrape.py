"""
This module provides functions to fetch course data from the UNSW Handbook API,
clean and process the data, and generate summaries for courses.

This module webscrapes all UNSW course names.

Note: This module was not used in the final product. This is because we are unable to
Webscrape all UNSW courses so we have then extract skills, knowledge and topics
from them. The UNSW course outline website is dynamically loaded so with over 6000
courses in total, this can take up to 35,000 minutes. 
"""

import re
import pandas as pd
import requests
import json
import sys


def fetch_course_data(api_url):
    """
    Fetches course data from the specified API URL.

    Parameters:
    - api_url (str): The URL of the API to fetch course data from.

    Returns:
    - dict: The JSON data containing course information.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        sys.exit(1)


def fetch_courses(base_url):
    """
    Fetches and processes course codes and titles from the UNSW Handbook API.

    Parameters:
    - base_url (str): The base URL of the UNSW Handbook API.

    Returns:
    - list: A list of unique course codes and titles.
    """
    # Fetch course data
    course_data = fetch_course_data(base_url)

    # Extract course codes and titles from the JSON data
    courses = []
    for course in course_data.get("contentlets", []):
        course_code = course["code"]
        course_title = course["title"]
        if course_code.startswith("COMP"):
            courses.append(f"{course_code} {course_title}")

    # Remove duplicates and sort the courses
    courses = sorted(set(courses))

    return courses

def remove_uncommon_symbols(input_string):
    """
    Removes uncommon symbols from a string.

    Parameters:
    - input_string (str): The input string containing symbols to be removed.

    Returns:
    - str: The cleaned string with uncommon symbols removed.
    """
    # Define a regular expression pattern to match uncommon symbols (e.g., anything not in [a-zA-Z0-9 ] or common punctuation)
    pattern = r'[^a-zA-Z0-9 \.,!?;:"]'

    # Use re.sub() to replace uncommon symbols with an empty string
    cleaned_string = re.sub(pattern, "", input_string)

    # Capitalize the first letter of each sentence
    cleaned_string = re.sub(
        r"([.!?]\s*)([a-z])", lambda x: x.group(1) + x.group(2).upper(), cleaned_string
    )

    # Remove extra spaces
    cleaned_string = re.sub(r"\s+", " ", cleaned_string)

    return cleaned_string


def get_course_summary(row, course_type, course_type_short):
    """
    Fetches course descriptions and cleans the text.

    Parameters:
    - row (pd.Series): A row from a Pandas DataFrame representing a course.
    - course_type (str): The type of course (e.g., "undergraduate" or "postgraduate").
    - course_type_short (str): The short code for the course type (e.g., "ugrd" or "pgrd").

    Returns:
    - str: The cleaned course summary text.
    """
    course = row["Course Code"]

    base_url = f"https://www.handbook.unsw.edu.au/api/content/render/false/query/+unsw_psubject.implementationYear:2024%20+unsw_psubject.studyLevel:{course_type}%20+unsw_psubject.active:1%20+unsw_psubject.studyLevelValue:{course_type_short}%20+unsw_psubject.code:{course}%20+deleted:false%20+working:true%20+live:true"

    response = requests.get(base_url)

    if response.status_code == 200:
        data = json.loads(response.text)
        course_data = data.get("contentlets", [])[0]
        course_description = course_data.get("description", "")
        # text = re.sub(r'[^\w\s.,;:!?()\'"â€™Â]', ' ', course_description)
        # text = re.sub(r'\s+', ' ', text)
        text = re.sub(r"\s+$", "", course_description, flags=re.MULTILINE)
        text = re.sub(r"<[p|ul]+>|</[p|ul]+>", "", text)
        text = re.sub(r"</li><li>", ", ", text)
        text = re.sub(r"</li>|<li>", "", text)

        # Remove &# (HTML entities)
        text = re.sub(r"&#\d+;", "", text)

        # Remove <div> tags
        text = re.sub(r"<div>|</div>", "", text)
        text = re.sub(r"<em>|</em>", "", text)
        text = text.replace("Â", "")
        text = re.sub(r"</?strong>", "", text)
        text = (
            text.replace("â€™", "")
            .replace("â€œ", "")
            .replace("â€", "")
            .replace("â€“", "")
        )
        text = text.strip()
        text = remove_uncommon_symbols(text)
        return text
    else:
        return "No course summary available"


# This is the driver code for to webscrape all UNSW courses

YEAR = 2024

# Define the base API URL for all courses
undergrad_url = f"https://www.handbook.unsw.edu.au/api/content/render/false/query/+unsw_psubject.implementationYear:{YEAR}%20+unsw_psubject.studyLevel:undergraduate%20+unsw_psubject.active:1%20+unsw_psubject.studyLevelValue:ugrd%20+deleted:false%20+working:true%20+live:true/orderby/unsw_psubject.code%20asc/limit/10000/offset/0"
postgrad_url = f"https://www.handbook.unsw.edu.au/api/content/render/false/query/+unsw_psubject.implementationYear:{YEAR}%20+unsw_psubject.studyLevel:postgraduate%20+unsw_psubject.active:1%20+unsw_psubject.studyLevelValue:pgrd%20+deleted:false%20+working:true%20+live:true/orderby/unsw_psubject.code%20asc/limit/10000/offset/0"

undergrad_courses = fetch_courses(undergrad_url)
postgrad_courses = fetch_courses(postgrad_url)

# Create a list of dictionaries
udrg_courses = [
    {"Course Code": course.split()[0], "Course Name": " ".join(course.split()[1:])}
    for course in undergrad_courses
]
pgrd_courses = [
    {"Course Code": course.split()[0], "Course Name": " ".join(course.split()[1:])}
    for course in postgrad_courses
]

# Create a DataFrame
df_udrg = pd.DataFrame(udrg_courses)
df_pgrd = pd.DataFrame(pgrd_courses)

df_udrg["Course Summary"] = df_udrg.apply(
    get_course_summary, axis=1, args=("undergraduate", "ugrd")
)
df_udrg.to_csv("undergrad_courses.csv", index=False)

df_pgrd["Course Summary"] = df_pgrd.apply(
    get_course_summary, axis=1, args=("postgraduate", "pgrd")
)
df_pgrd.to_csv("postgrad_courses.csv", index=False)
