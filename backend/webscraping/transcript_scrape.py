"""
This script helps with scraping all courses a student has completed from their
UNSW academic transcript in the form of [course_code, year, term/semester]
"""
import re
from io import BytesIO
import base64
import PyPDF2


def scrape_pdf_from_base64(base64_string):
    """
    Extracts data from a base64-encoded PDF string and organizes information related to courses.

    Parameters:
    - base64_string (str): A base64-encoded string representing a PDF document.

    Returns:
    list: A list of lists containing details about courses with the format [course_code,
    year, semester].
    """
    if "data:application/pdf;base64," in base64_string:
        base64_string = base64_string.replace("data:application/pdf;base64,", "")

    pdf_binary_data = base64.b64decode(base64_string)

    # Create a BytesIO object to simulate a file-like object from binary data
    pdf_file = BytesIO(pdf_binary_data)

    # Create a PyPDF2 PdfFileReader object to read the PDF
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    transcript_content = []

    # Iterate through the pages in the PDF
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        page_text = page.extract_text()
        transcript_content.append(page_text)

    # Join the list of page texts into a single string
    all_text = "\n".join(transcript_content)

    all_term_data = []
    term_data = []
    tag = ""

    list_text = all_text.split("\n")

    for line in list_text:
        if "Term WAM" in line:
            continue
        if line.startswith("Semester") or line.startswith("Term"):
            tag = line.strip()
        elif line.strip() and tag:
            line_with_tag = f"{line.strip()} - {tag}"
            term_data.append(line_with_tag)

        # Check if a new tag is encountered
        if line.startswith("Semester") or line.startswith("Term"):
            if term_data:
                all_term_data.append(term_data)
                term_data = []

    # Append the last term data if the list is not empty
    if term_data:
        all_term_data.append(term_data)

    # Print the organized term data
    all_term_data = [line for sublist in all_term_data for line in sublist]
    all_term_data = "\n".join(all_term_data)

    # Define a regular expression pattern to find lines containing "6.00 6.00"
    pattern = r".*6.00 6.00.*"

    # Find and capture lines containing "6.00 6.00"
    lines_with_6_00 = re.findall(pattern, all_term_data)

    extracted_data = []

    # Iterate through the data and extract the desired components
    for line in lines_with_6_00:
        line = line.replace("  ", " ")
        print(line)
        line = line.strip()
        course_code = line[:10]
        course_code = course_code.replace(" ", "").strip()
        term_year = line[-11:]
        year = term_year[-4:]
        semester = term_year[:6]

        details = []
        details.append(course_code)
        details.append(year)
        details.append(semester)
        extracted_data.append(details)

    print(extracted_data)
    return extracted_data
