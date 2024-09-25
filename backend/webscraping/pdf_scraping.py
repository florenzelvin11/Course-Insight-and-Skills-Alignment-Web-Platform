"""
Given a pdf will scrape out all the information required by a course page
including course code, course name, course school, course type, course
description, course aims, course outcomes, course schedule, course general
schecule, course year, course term and scrape timestamp. Then NLP is applied
to extract skills, knowledge and topics.
"""
from datetime import datetime
from io import BytesIO
import base64
import re
import PyPDF2
from webscraping.scrape_single_course import (
    get_course_topics,
    find_closest_match,
    get_skills_and_knowledge,
)


def remove_print_tags(content, course_code, course_name):
    """
    Removes print tags from a given content based on the provided course code and course name.

    This function uses a regular expression pattern to locate and remove specific print tags
    associated with a given course identified by its course code and course name.

    Parameters:
    - content (str): The original content containing print tags.
    - course_code (str): The course code for which print tags should be removed.
    - course_name (str): The course name corresponding to the provided course code.

    Returns:
    str: The content with print tags related to the specified course removed.
    """
    pattern = (
        re.escape(course_code + " " + course_name) + r" - (\d{4}) (.*?) \| (\d+ of \d+)"
    )
    # Use re.sub to remove the matched text
    result = re.sub(pattern, "", content)
    return result


def scrape_pdf(base64_string):
    """
    Extracts text content from a base64-encoded PDF string.

    This function takes a base64-encoded string representing a PDF document, decodes it,
    and extracts text content from each page of the PDF. The extracted content is returned as
    a list where each element represents the text content of a page.

    Parameters:
    - base64_string (str): A base64-encoded string representing a PDF document.

    Returns:
    list: A list of strings where each element corresponds to the text content of a page in the PDF.
    """

    if "data:application/pdf;base64," in base64_string:
        base64_string = base64_string.replace("data:application/pdf;base64,", "")

    pdf_binary_data = base64.b64decode(base64_string)

    # Create a BytesIO object to simulate a file-like object from binary data
    pdf_file = BytesIO(pdf_binary_data)

    # Create a PyPDF2 PdfFileReader object to read the PDF
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    course_content = []

    # Iterate through the pages in the PDF
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        page_text = page.extract_text()
        course_content.append(page_text)

    return course_content


def extract_course_pdf(course_content):
    """
    Extracts information from a PDF course content.

    This function takes the text content of a course PDF and extracts various pieces of
    information such as course code, course name, academic unit, study level, course description,
    course aims, course learning outcomes, course schedule, and general schedule information.

    Parameters:
    - course_content (list): A list of strings where each element corresponds to the text content
    of a PDF page.

    Returns:
    dict: A dictionary containing extracted information about the course.
    """
    # Join the list of page texts into a single string
    all_text = "\n".join(course_content)

    # Define regular expressions to match Course Code and Year
    course_code_pattern = r"Course Code\s*:\s*(\w+)"
    year_pattern = r"Year\s*:\s*(\d{4})"

    # Search for matches
    course_code_match = re.search(course_code_pattern, all_text)
    year_match = re.search(year_pattern, all_text)

    # Extract values if matches are found
    course_code = course_code_match.group(1) if course_code_match else "N/A"
    year = year_match.group(1) if year_match else "N/A"

    pattern = r"Academic Unit\s*:\s*(.*?)\n"

    # Use re.search to find the first match
    match = re.search(pattern, all_text)

    academic_unit = match.group(1).strip()

    # Define regular expressions to match Term and Study Level
    term_pattern = r"Term\s*:\s*(\w+\s+\d+)"
    study_level_pattern = r"Study Level\s*:\s*(\w+)"
    topic_pattern = r"Topic \d+:"

    # Search for matches
    term_match = re.search(term_pattern, all_text)
    study_level_match = re.search(study_level_pattern, all_text)

    # Extract values if matches are found
    term = term_match.group(1) if term_match else "N/A"
    if term == "Term 3":
        term = "T3"
    elif term == "Term 2":
        term = "T2"
    elif term == "Term 2":
        term = "T2"

    study_level = study_level_match.group(1) if study_level_match else "N/A"

    pattern = rf"{course_code} (.*?) - {year}"

    # Search for matches
    match = re.search(pattern, all_text)

    # Extract the text if a match is found
    if match:
        course_name = match.group(1)

    # Use regular expressions to extract the desired text
    course_description = re.search(
        r"Course Description(.*?)Course Aims", all_text, re.DOTALL
    )

    if not course_description:
        course_description = re.search(
            r"Course Description(.*?)Course Learning Outcomes", all_text, re.DOTALL
        )

    # Check if the match was found
    course_description_text = ""
    if course_description:
        course_description_text = course_description.group(1).strip()
        course_description_text = remove_print_tags(
            course_description_text, course_code, course_name
        )
        course_description_text = re.sub(topic_pattern, "", course_description_text)

    # Use regular expressions to extract the desired text
    course_aims = re.search(
        r"Course Aims(.*?)Course Learning Outcomes", all_text, re.DOTALL
    )

    # Check if the match was found
    course_aims_text = ""
    if course_aims:
        course_aims_text = course_aims.group(1).strip()
        course_aims_text = remove_print_tags(course_aims_text, course_code, course_name)
        course_aims_text = re.sub(topic_pattern, "", course_aims_text)

    # Use regular expressions to extract the desired text
    course_outcomes = re.search(
        r"Course Learning Outcomes(.*?)Course Learning Outcomes Assessment Item",
        all_text,
        re.DOTALL,
    )

    # Check if the match was found
    course_outcomes_text = course_outcomes.group(1).strip()
    course_outcomes_text = course_outcomes_text.split("\n")
    new_course_outcomes = []

    # Initialize a variable to store the current CLO line
    current_clo_line = ""

    for line in course_outcomes_text:
        if course_name in line:
            continue
        # Check if the line starts with "CLO"
        if line.startswith("CLO"):
            # If there's a current CLO line, add it to the new_course_outcomes list
            if current_clo_line:
                new_course_outcomes.append(current_clo_line)
            # Set the current CLO line to the current line
            current_clo_line = line
        else:
            # If the line doesn't start with "CLO," append it to the current CLO line
            current_clo_line += "" + line

    # Add the last CLO line
    if current_clo_line:
        new_course_outcomes.append(current_clo_line)

    # Join the modified lines with '\n' to form the final text
    course_outcomes_text = "\n".join(new_course_outcomes)

    # Use regular expressions to extract the desired text
    course_schedule = re.search(
        r"Course Schedule(.*?)Attendance Requirements", all_text, re.DOTALL
    )

    # Check if the match was found
    course_schedule_text = ""
    if course_schedule:
        course_schedule_text = course_schedule.group(1).strip()
        course_schedule_text = (
            course_schedule_text.replace("Tutorial", "")
            .replace("Lecture", "")
            .replace("Laboratory", "")
        )
        course_schedule_text = remove_print_tags(
            course_schedule_text, course_code, course_name
        )
        course_schedule_text = re.sub(topic_pattern, "", course_schedule_text)

    # Use regular expressions to extract the desired text
    course_general_schedule = re.search(
        r"General Schedule Information(.*?)Course Resources", all_text, re.DOTALL
    )

    # Check if the match was found
    course_general_schedule_text = ""
    if course_general_schedule:
        course_general_schedule_text = course_general_schedule.group(1).strip()
        course_general_schedule_text = remove_print_tags(
            course_general_schedule_text, course_code, course_name
        )
        course_general_schedule_text = re.sub(
            topic_pattern, "", course_general_schedule_text
        )

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    all_info = {
        "course": course_code,
        "course_name": course_name,
        "course_school": find_closest_match(academic_unit),
        "course_type": study_level,
        "course_description": course_description_text,
        "course_aims": course_aims_text,
        "course_outcomes": course_outcomes_text,
        "course_schedule": course_schedule_text,
        "course_general_schedule": course_general_schedule_text,
        "course_year": year,
        "course_term": term,
        "course_scraped": formatted_datetime,
    }

    return all_info


def get_single_course_information_from_pdf(pdf_path):
    """
    Extracts and processes information from a course PDF.

    This function takes the path to a course PDF, extracts relevant information using the
    `extract_course_pdf` function, and further processes the data to obtain skills, knowledge,
    and course topics. The processed information is added to the original data and returned.

    Parameters:
    - pdf_path (str): The file path to the course PDF.

    Returns:
    dict: A dictionary containing extracted and processed information about the course.
    """
    raw_scraped_data = extract_course_pdf(pdf_path)

    keys_to_get = [
        "course_description",
        "course_aims",
        "course_outcomes",
        "course_schedule",
        "course_general_schedule",
    ]
    course_outline_info = [raw_scraped_data[key] for key in keys_to_get]
    course_outline_info = "\n".join(course_outline_info)
    skills, knowledge = get_skills_and_knowledge(course_outline_info)

    raw_scraped_data["course_skills"] = skills
    raw_scraped_data["course_knowledge"] = knowledge

    course_topics = get_course_topics(raw_scraped_data)
    raw_scraped_data["course_topics"] = course_topics

    return raw_scraped_data
