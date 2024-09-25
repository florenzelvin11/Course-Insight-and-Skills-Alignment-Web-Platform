from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from collections import Counter
import difflib
import os
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from IPython.core.display import HTML
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
import re
import string
import pandas as pd
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

schools = [
    "Australian Graduate School of Management",
    "School of Accounting, Auditing and Taxation",
    "School of Banking and Finance",
    "School of Economics",
    "School of Information Systems and Technology Management",
    "School of Management and Governance",
    "School of Marketing",
    "UNSW Business School",
    "School of Risk and Actuarial Studies",
    "Graduate School of Biomedical Engineering",
    "School of Chemical Engineering",
    "School of Civil and Environmental Engineering",
    "School of Computer Science and Engineering",
    "School of Electrical Engineering and Telecommunications",
    "School of Mechanical and Manufacturing Engineering",
    "School of Minerals and Energy Resources Engineering",
    "School of Photovoltaic and Renewable Energy Engineering",
    "School of Art and Design",
    "School of the Arts and Media",
    "School of Built Environment",
    "School of Social Sciences",
    "School of Humanities and Languages",
    "School of Education",
    "School of Law, Society and Criminology",
    "School of Global and Public Law",
    "School of Private and Commercial Law",
    "School of Clinical Medicine",
    "School of Population Health",
    "School of Health Sciences",
    "School of Optometry and Vision Science",
    "School of Biomedical Sciences",
    "School of Aviation",
    "School of Biological, Earth and Environmental Sciences",
    "School of Biotechnology and Biomolecular Sciences",
    "School of Chemistry",
    "School of Materials Science and Engineering",
    "School of Mathematics and Statistics",
    "School of Physics",
    "School of Psychology",
]


def find_closest_match(scraped_school):
    '''
    This function finds the closest matching school name from a list of known school names.

    Parameters:
    - scraped_school (str): The school name to find the closest match for.
    
    Returns:
    - str: The closest matching school name from the list. If no close match is found, 
    the original scraped school name is returned.
    '''
    closest_match = difflib.get_close_matches(scraped_school, schools, n=1, cutoff=0.6)
    if closest_match:
        return closest_match[0]
    else:
        return scraped_school


def get_single_paragraph(path, driver):
    try:
        paragraph_element = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        paragraph_text = paragraph_element.text
        return paragraph_text
    except Exception as e:
        pass


def get_school(url):
    '''
    This function retrieves the text content of a single paragraph identified by its XPath on a webpage using a Selenium WebDriver.

    Parameters:
    - path (str): XPath expression to locate the paragraph element on the webpage.
    - driver (WebDriver): An instance of the Selenium WebDriver used for web scraping.

    Returns:
    - str: The text content of the identified paragraph.
    '''
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver_course = webdriver.Chrome(options=chrome_options)

    driver_course.get(url)

    # Course School
    course_school = ""
    course_title_school = f"/html/body/div[4]/div/div[9]/div/div[1]/div/div[3]/span/div/div[4]/ul/li/dl/div[1]/div[3]/dd"
    try:
        paragraph_element = WebDriverWait(driver_course, 50).until(
            EC.presence_of_element_located((By.XPATH, course_title_school))
        )
        paragraph_text = paragraph_element.text
        course_school = paragraph_text
        print(paragraph_element.text)
    except Exception as e:
        pass

    return course_school.strip()


def scrape_raw_course_data(url):
    '''
    This function performs web scraping to extract raw course data from a given URL.
    It uses Selenium with Chrome WebDriver in headless mode to interact with the webpage.

    Parameters:
    - url (str): The URL of the course outline page.

    Returns:
    - dict: A dictionary containing various information about the course,
    including course code, name, school, type, description, aims, outcomes,
    schedules, year, term, and scraping timestamp.
    '''
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    try:
        button = driver.find_element(
            By.XPATH,
            "/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/button",
        )
        button.click()
    except Exception as e:
        pass

    paragraph_counter = 1
    course_description = []
    # Loop until there are no more paragraphs
    while True:
        paragraph_xpath = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[3]/span/div/div/p[{paragraph_counter}]"

        try:
            paragraph_element = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, paragraph_xpath))
            )
            paragraph_text = paragraph_element.text
            course_description.append(paragraph_text)
            # Increment the counter to check the next paragraph
            paragraph_counter += 1
        except Exception as e:
            break

    course_description = [item for item in course_description if item != ""]

    if len(course_description) == 0:
        paragraph_xpath = "/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[3]/span/div/div/p"
        paragraph = get_single_paragraph(paragraph_xpath, driver)
        course_description.append(paragraph)

    dot_point_num = 1
    while True:
        dot_points = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[3]/span/div/div/ul/li[{dot_point_num}]"

        try:
            paragraph_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, dot_points))
            )
            paragraph_text = paragraph_element.text
            course_description.append(paragraph_text)
            dot_point_num += 1
        except Exception as e:
            break

    # Get course description
    # print("Course Description")
    course_description = []

    paragraph_counter = 1
    # Loop until there are no more paragraphs
    while True:
        paragraph_xpath = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[3]/span/div/div/p[{paragraph_counter}]"

        try:
            paragraph_element = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, paragraph_xpath))
            )
            paragraph_text = paragraph_element.text
            course_description.append(paragraph_text)
            # Increment the counter to check the next paragraph
            paragraph_counter += 1
        except Exception as e:
            break

    course_description = [item for item in course_description if item != ""]

    if len(course_description) == 0:
        paragraph_xpath = "/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[3]/span/div/div/p"
        paragraph = get_single_paragraph(paragraph_xpath, driver)
        course_description.append(paragraph)

    dot_point_num = 1
    while True:
        dot_points = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[3]/span/div/div/ul/li[{dot_point_num}]"
        try:
            paragraph_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, dot_points))
            )
            paragraph_text = paragraph_element.text
            course_description.append(paragraph_text)
            dot_point_num += 1
        except Exception as e:
            break

    # for paragraph in course_description:
    #     print(paragraph)
    course_description = [item for item in course_description if item is not None]
    course_description = "\n".join(course_description)

    # Get Course Aims
    course_aims = []
    # print("\nCourse Aims")
    paragraph_counter = 1

    # Loop until there are no more paragraphs
    while True:
        paragraph_xpath = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[4]/span/div/div/p[{paragraph_counter}]"

        try:
            paragraph_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, paragraph_xpath))
            )

            paragraph_text = paragraph_element.text
            course_aims.append(paragraph_text)

            # Increment the counter to check the next paragraph
            paragraph_counter += 1
        except Exception as e:
            break

    course_aims = [item for item in course_aims if item != ""]

    if len(course_aims) == 0:
        paragraph_xpath = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[4]/span/div/div/p"
        paragraph = get_single_paragraph(paragraph_xpath, driver)
        course_aims.append(paragraph)

    dot_point_num = 1
    while True:
        dot_points = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[4]/span/div/p/ul/li[{dot_point_num}]"
        try:
            paragraph_element = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.XPATH, dot_points))
            )
            paragraph_text = paragraph_element.text
            course_aims.append(paragraph_text)
            dot_point_num += 1
        except Exception as e:
            break

    # for paragraph in course_aims:
    #     print(paragraph)
    course_aims = [item for item in course_aims if item is not None]
    course_aims = "\n".join(course_aims)

    # Get Course Outcomes
    # print("\nOutcomes")
    course_outcomes = ""
    outcomes = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[7]/span/div"
    try:
        paragraph_element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, outcomes))
        )
        paragraph_text = paragraph_element.text
        course_outcomes = paragraph_text
    except Exception as e:
        pass

    button_topics = driver.find_element(
        By.XPATH,
        "/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[8]/button",
    )
    button_topics.click()

    # Course Schedule
    number = 1
    topics = []
    consecutive_exceptions = 0  # Initialize the consecutive exceptions counter
    max_consecutive_exceptions = 5  # Set the maximum consecutive exceptions threshold

    while True:
        # Construct the XPath dynamically with the current number
        xpath = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[8]/div/div/span/div/div/div[4]/span/div/ul/li[{number}]/dl/div[3]/dd"
        # Try to locate the element
        try:
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            element_text = element.text
            topics.append(element_text)
            number += 1
            consecutive_exceptions = 0  # Reset the consecutive exceptions counter
        except Exception as e:
            number += 1
            consecutive_exceptions += 1  # Increment the consecutive exceptions counter
            if consecutive_exceptions > max_consecutive_exceptions:
                break

    unique_topics_list = []

    for topic in topics:
        if topic not in unique_topics_list:
            unique_topics_list.append(topic)

    phrases_to_remove = [
        "midterm exam",
        "final exam",
        "midterm quiz",
        "tbd",
        "assignment",
        "flexibility week",
        "nothing",
    ]
    unique_topics_list = [
        topic
        for topic in unique_topics_list
        if all(phrase not in topic for phrase in phrases_to_remove)
    ]
    unique_topics_list = [topic.strip() for topic in unique_topics_list]

    unique_topics_list.sort()

    # print("\nTopics")
    # for topic in unique_topics_list:
    #     print(topic)
    unique_topics_list = [item for item in unique_topics_list if item is not None]
    course_schedule = "\n".join(unique_topics_list)

    # Course General topics
    course_general_schedule = ""
    course_general_topics = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[8]/div/div/span/div/div/div[6]/span/div"
    try:
        paragraph_element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, course_general_topics))
        )
        paragraph_text = paragraph_element.text
        course_general_schedule = paragraph_text
    except Exception as e:
        pass

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Parse the URL
    parsed_url = urlparse(url)

    # Extract query parameters
    query_params = parse_qs(parsed_url.fragment)

    # Extract the desired information
    year = query_params.get("year", [""])[0]
    term = query_params.get("term", [""])[0]
    course_code = query_params.get("courseCode", [""])[0]
    activity_group_id = query_params.get("activityGroupId", [""])[0]

    # Determine if it's an undergraduate or postgraduate course based on the activity group ID
    course_type = "Undergraduate" if activity_group_id == "1" else "Postgraduate"

    course_title = f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[1]/div/div[1]/h1"

    # Course General topics
    course_title = ""
    course_title_address = (
        f"/html/body/div[4]/div/div[4]/div/div[1]/div/div[1]/div/div[1]/h1"
    )
    try:
        paragraph_element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, course_title_address))
        )
        paragraph_text = paragraph_element.text
        course_title = paragraph_text
        course_title = (
            course_title.replace(course_code, "").replace(year, "").replace("-", "")
        )
    except Exception as e:
        pass

    search_link = f"https://www.unsw.edu.au/course-outlines#search={course_code.strip()}&filters=year%3A{year}&sort=relevance&startRank=1&numRanks=10"

    course_school = get_school(search_link)

    all_info = {
        "course": course_code,
        "course_name": course_title,
        "course_school": find_closest_match(course_school),
        "course_type": course_type,
        "course_description": course_description,
        "course_aims": course_aims,
        "course_outcomes": course_outcomes,
        "course_schedule": course_schedule,
        "course_general_schedule": course_general_schedule,
        "course_year": year,
        "course_term": term[0]+term[-1],
        "course_scraped": formatted_datetime,
    }

    driver.quit()
    return all_info


remove_list = [
    "cse",
    "learning outcomes",
    "vscode",
    "lecture",
    "tutorials",
    "tutorial",
    "lecture",
    "tutorials",
    "instructions",
    "stages",
    "instruct",
    "instructions",
    "human",
    "technology battery",
    "knowledge base",
    "equal",
    "final",
    "www",
    "pdf",
]

soft_skills_list = [
    "communication",
    "teamwork",
    "problem solving",
    "leadership",
    "adaptability",
    "critical thinking",
    "creativity",
    "time management",
    "logical thinking",
    "collaboration",
    "resilience",
    "reading",
    "scheduling",
    "decision making",
    "social networking",
    "essay writing",
    "making decision",
    "teaching",
    "planning",
    "writing",
    "mobile device abilities",
]


def convert_similar_to_exact_soft_skills(skill_set, soft_skills_list):
    """
    Converts skills in a given skill set to exact soft skills based on similarity.

    Parameters:
    - skill_set (set): A set of skills to be converted.
    - soft_skills_list (list): A list of known soft skills for comparison.

    Returns:
    - list: A list of converted soft skills and original skills.
    """
    skill_list = list(skill_set)
    converted_skills = []

    for skill in skill_list:
        if len(skill) == 1 or skill in remove_list:
            continue
        if any(char.isdigit() for char in skill):
            continue
        is_converted = False
        for soft_skill in soft_skills_list:
            similarity = fuzz.token_sort_ratio(skill, soft_skill)
            if similarity >= 50:
                converted_skills.append(soft_skill)
                is_converted = True
                break
            if skill.lower().startswith("and"):
                # Remove "and" from the beginning
                skill = skill[len("and") :].strip()
        if not is_converted:
            converted_skills.append(skill)

    return converted_skills


def remove_similar_duplicates(skill_set):
    """
    Removes similar duplicates from a set of skills.

    Parameters:
    - skill_set (set): A set of skills to process.

    Returns:
    - set: A set of skills with similar duplicates removed.
    """
    skill_list = list(skill_set)
    duplicates_removed = set()

    for skill in skill_list:
        if len(skill) == 1 or skill in remove_list:
            continue
        if any(char.isdigit() for char in skill):
            continue
        skill_as_list = skill.split()
        skill_as_list = set(skill_as_list)
        skill_as_list = list(skill_as_list)
        skill = " ".join(skill_as_list)
        is_duplicate = False
        for existing in duplicates_removed:
            similarity = fuzz.token_sort_ratio(skill, existing)
            if similarity >= 80:
                is_duplicate = True
                break

        if not is_duplicate:
            duplicates_removed.add(skill)

    return duplicates_removed


def merge_similar_skills(skill_set):
    """
    Merges similar skills from a set of skills.

    Parameters:
    - skill_set (set): A set of skills to process.

    Returns:
    - set: A set of skills with similar skills merged.
    """
    skill_list = list(skill_set)
    merged_skills = set()
    for skill in skill_list:
        skill = skill.replace("continue", "").strip()
        if len(skill) == 1 or skill in remove_list:
            continue
        if any(char.isdigit() for char in skill):
            continue
        skill_as_list = skill.split()
        skill_as_list = set(skill_as_list)
        skill_as_list = list(skill_as_list)
        skill = " ".join(skill_as_list)
        is_similar = False
        for existing in merged_skills:
            similarity = fuzz.token_sort_ratio(skill, existing)
            if similarity >= 80:
                skill = existing  # Change to the same word
                is_similar = True
                break
        if not is_similar:
            merged_skills.add(skill)

    return merged_skills


def normalize_counts_to_percentages(data):
    """
    Normalizes counts in a data set to percentages.

    Parameters:
    - data (list): A list of dictionaries, where each dictionary represents an item with a 'count' attribute.

    Returns:
    - list: A modified list of dictionaries with normalized percentages ('weight') and 'count' removed.
    """
    # Calculate the total count
    total_count = sum(item["count"] for item in data)

    for item in data:
        item["weight"] = round((item["count"] / total_count) * 100)

    for item in data:
        del item["count"]

    return data


def get_skills_and_knowledge(course_outline):
    '''
    Extract all skills and knowledge from a 'comp_courses.csv' and put 
    those skills and knowledge as seperate columns in a csv called 
    'comp_courses_with_skills.csv'

    '''

    nlp = spacy.load("en_core_web_lg")
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    skills_and_knowledge = skill_extractor.annotate(course_outline)

    full_matches = skills_and_knowledge["results"]["full_matches"]
    ngram_scored = skills_and_knowledge["results"]["ngram_scored"]

    full_match_skills = [match["doc_node_value"] for match in full_matches]
    ngram_scored_skills = [ngram["doc_node_value"] for ngram in ngram_scored]

    all_skills = full_match_skills + ngram_scored_skills

    html_output = skill_extractor.describe(skills_and_knowledge)
    html_string = html_output.data

    # # Parse the HTML content
    soup = BeautifulSoup(html_string, "html.parser")

    # Find all spans with class 'text-xs text-white font-bold'
    skill_spans = soup.find_all("span", class_="text-xs text-white font-bold")

    # Open a file in write mode to save the results
    with open("output.txt", "w", encoding="utf-8") as output_file:
        for skill_span in skill_spans:
            # Extract the skill word and its type (e.g., Hard Skill or Soft Skill)
            skill_text = skill_span.parent.text.strip()  # Extract the full text
            skill_type = (
                skill_span.text.strip()
            )  # Extract the skill type (Hard Skill or Soft Skill)

            # Write the skill word and its type to the file
            output_file.write("Skill Word: {}\n".format(skill_text))
            output_file.write("Skill Type: {}\n\n".format(skill_type))

    # Read the text from a file
    with open("output.txt", "r") as file:
        text = file.readlines()

    # Use a loop to check each line for trailing spaces
    results = []
    for line in text:
        if not line.startswith(" "):
            results.append(line)

    filtered_lines = [line.strip() for line in results if line.strip()]

    # Initialize an empty list to store tuples
    result = []

    # Iterate through the list two items at a time and create tuples
    for i in range(0, len(filtered_lines), 2):
        if i + 1 < len(filtered_lines):
            item1 = filtered_lines[i]
            item2 = filtered_lines[i + 1]
            result.append((item1, item2))

    soft_skills = []
    hard_skills = []

    for skill_word, skill_type in result:
        # Remove 'Skill Word' from skill descriptions
        skill_word = skill_word.replace("Skill Word: ", "")

        if "Soft Skill" in skill_type:
            soft_skills.append(skill_word)
        elif "Hard Skill" in skill_type:
            hard_skills.append(skill_word)

    soft_skills = convert_similar_to_exact_soft_skills(soft_skills, remove_list)
    hard_skills = convert_similar_to_exact_soft_skills(hard_skills, remove_list)

    soft_skills = convert_similar_to_exact_soft_skills(soft_skills, soft_skills_list)
    hard_skills = convert_similar_to_exact_soft_skills(hard_skills, soft_skills_list)

    # Remove similar duplicates in both soft and hard skills
    soft_skills_cleaned = merge_similar_skills(soft_skills)
    hard_skills_cleaned = merge_similar_skills(hard_skills)

    soft_skills_cleaned = convert_similar_to_exact_soft_skills(
        soft_skills_cleaned, soft_skills_list
    )
    hard_skills_cleaned = convert_similar_to_exact_soft_skills(
        hard_skills_cleaned, soft_skills_list
    )

    # Move skills to their respective lists
    for skill in soft_skills_list:
        if skill in hard_skills_cleaned:
            while skill in hard_skills_cleaned:
                hard_skills_cleaned.remove(skill)
                soft_skills_cleaned.append(skill)

    soft_skills_cleaned = Counter(soft_skills_cleaned)
    soft_skills_cleaned = [
        {"name": item, "count": count} for item, count in soft_skills_cleaned.items()
    ]
    soft_skills_cleaned = normalize_counts_to_percentages(soft_skills_cleaned)
    soft_skills_cleaned = {item["name"]: item["weight"] for item in soft_skills_cleaned}

    hard_skills_cleaned = Counter(hard_skills_cleaned)
    hard_skills_cleaned = [
        {"name": item, "count": count} for item, count in hard_skills_cleaned.items()
    ]
    hard_skills_cleaned = normalize_counts_to_percentages(hard_skills_cleaned)
    hard_skills_cleaned = {item["name"]: item["weight"] for item in hard_skills_cleaned}

    os.remove("output.txt")
    return soft_skills_cleaned, hard_skills_cleaned


def get_topics(text):
    """
    Extracts topics from a given text using a regular expression pattern.

    Parameters:
    - text (str): The input text from which topics are to be extracted.

    Returns:
    - list: A list of extracted topics.
    """
    pattern = r"Topics:\s*(.*?)(?=\n\n|$)"

    # Use re.findall to find all matching lines
    if text is not None and not isinstance(text, str):
        text = str(text)
    matches = re.findall(pattern, text, re.DOTALL)

    # Extracted topics
    if matches:
        topics = [match.strip() for match in matches]
    else:
        topics = []

    return topics


words_to_remove = set(
    [
        "Term Break (Flex Week)",
        "Flexibility Week",
        "Course Overview",
        "Introduction",
        "Course Intro",
        "Getting Started",
        "Contest",
        "ICPC Preliminary Contest",
        "Problem Set released",
        "TBA",
        "Exam Revision",
        "Exam",
        "Final Examination",
        "Mid Term Examination",
        "Lecture",
        "Lab",
        "Public holiday",
        "Project",
        "Assignment",
        "Essay",
        "Quiz is due",
        "Quiz",
        "Assessment",
        "Course Overview",
        "Nothing",
        "Fortnightly",
        "Weekly",
        "No Content",
        "course outline",
        "IEEE754 UTF8",
        "NonExaminable",
        "NO LECTURE NO Tutorials NO Labs",
        "course content",
        "past exam questions",
        "Fortnightly quiz on material of Weeks",
        "Welcome",
        "no submission and no marks",
        "IPv6",
        "Email",
        "Tutorial",
        "Course prepration Optional",
        "Consultation Session",
        "Iteration",
        "Working as a team",
        "Assignments",
        "General Schedule Information" "Prac Work",
        "Lecture",
        "Weekly/fornightly meetings with your supervisor",
        "report",
        "Progressive Demo B Retrospective B",
        "due",
        "Review of the material",
        "Quiz Complete Lab",
        "Complete Lab1",
        "Midlecture Quiz Complete Lab",
        "Seminar",
        "This is a tentative schedule",
        "Teaching WeekModuleActivity TypeContent",
        "details",
    ]
)


def preprocess_text(text):
    """
    Preprocesses a given text by tokenizing, converting to lowercase, and removing stopwords.

    Parameters:
    - text (str): The input text to be preprocessed.

    Returns:
    - str: The preprocessed text.
    """
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stopwords.words("english")]
    return " ".join(tokens)


def is_similar(phrase):
    """
    Determines if a given phrase is similar to a predefined set of phrases.

    Parameters:
    - phrase (str): The input phrase to be checked for similarity.

    Returns:
    - bool: True if the phrase is similar, False otherwise.
    """
    processed_phrase = preprocess_text(phrase)

    for word in words_to_remove:
        processed_word = preprocess_text(word)

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(
            [processed_phrase, processed_word]
        )

        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)[0][1]
        if cosine_sim > 0.3:
            return True
    return False


def remove_punctuation(text):
    """
    Removes punctuation from a given text.

    Parameters:
    - text (str): The input text from which punctuation is to be removed.

    Returns:
    - str: The text with punctuation removed.
    """
    exclude = string.punctuation.replace("+", "").replace(
        "#", ""
    )  # Remove + and # from punctuation
    return "".join([char for char in text if char not in exclude])


def get_topics_from_schedule(text):
    """
    Extracts topics from a schedule text, removing similar and short topics.

    Parameters:
    - text (str): The input schedule text from which topics are to be extracted.

    Returns:
    - list: A list of extracted topics.
    """
    text = str(text)

    pattern = r"\d{1,2} \w+"
    cleaned_text = re.sub(pattern, "", text)

    cleaned_text = cleaned_text.split("\n")
    cleaned_text = set([i.strip() for i in cleaned_text])

    text = "\n".join(cleaned_text)
    lines = text.split("\n")

    lines = [item for item in lines if item != ""]

    for line in lines:
        if "-" in line:
            lecture_content = line.split("-")
            line = "\n".join(lecture_content[1:])
        if ":" in line:
            lecture_content = line.split(":")
            line = "\n".join(lecture_content[1:])

    filtered_lines = []

    for line in lines:
        if not is_similar(line) or len(line) < 80:
            filtered_lines.append(line)

    filtered_lines = [re.sub(r"\[.*?\]", "", item) for item in filtered_lines]
    filtered_lines = [remove_punctuation(item) for item in filtered_lines]

    return filtered_lines


def get_topics_clean_string(text):
    """
    Processes a list of text items, splitting them by commas and removing punctuation.

    Parameters:
    - text (list): The list of text items to be processed.

    Returns:
    - list: A list of cleaned topics.
    """
    all_topics = []

    for item in text:
        topics = [
            topic.strip() and remove_punctuation(topic) for topic in item.split(",")
        ]
        all_topics.extend(topics)

    return all_topics


def remove_days(text):
    """
    Removes days of the week from a given text.

    Parameters:
    - text (str): The input text from which days of the week are to be removed.

    Returns:
    - str: The text with days of the week removed.
    """
    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    day_pattern = r"\b(?:" + "|".join(map(re.escape, days_of_week)) + r")\b"
    return re.sub(day_pattern, "", text, flags=re.I)


def remove_week_num(text):
    """
    Removes week numbers from a list of text items.

    Parameters:
    - text (list): The list of text items from which week numbers are to be removed.

    Returns:
    - list: The list of text items without week numbers.
    """
    pattern = r"Week \d+ "
    week_strings_without_week = [re.sub(pattern, "", s) for s in text]
    return week_strings_without_week


def get_course_topics(course_info):
    """
    Processes a DataFrame containing course information and extracts course topics.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing course information.

    Returns:
    - pd.DataFrame: The original DataFrame with an additional 'topics' column.
    """
    course = course_info["course"]
    if course == "COMP9024":
        return "No Information about Topics"
    course_description = course_info["course_description"]
    course_aims = course_info["course_aims"]
    course_schedule = course_info["course_schedule"]
    course_general_schedule = course_info["course_general_schedule"]

    topics = get_topics(course_description)
    if topics == []:
        topics = get_topics(course_aims)
        if topics:
            topics = get_topics_clean_string(topics)

    if topics == []:
        topics = get_topics_from_schedule(course_schedule)
        if topics:
            topics = get_topics_clean_string(topics)

    if topics == ["nan"]:
        topics = get_topics_from_schedule(course_general_schedule)
    topics = set(topics)

    # regular expression pattern to match 'Ch' followed by numbers
    ch_pattern = r"\bCh \d+\b"

    topics = {
        item
        for item in topics
        if not re.search(ch_pattern, item) and not item.startswith("Fortnightly")
    }

    topics = remove_week_num(topics)
    topics = [re.sub(r"LEC\s+\d+\s+", "", item) for item in topics]
    topics = [remove_days(item) for item in topics]
    topics = [item for item in topics if not item.startswith("Quiz")]
    stop_words = [
        "Prac Work",
        "Lecture",
        "Review of the material",
        "live lecture",
        "via",
        "Blackboard collaborate" "Extended 6841 Seminar",
        "Regulation 3040 Seminar",
        "seL4",
        "Lectue ",
        "Setting up your environment",
    ]
    filtered_topics = []

    # Loop through the topics and remove stop words
    for topic in topics:
        for word in stop_words:
            topic = topic.replace(word, "")
        filtered_topics.append(topic)
    topics = [re.sub(r"Lab\d+\s", "", s) for s in filtered_topics]
    topics = [line for line in topics if "exam" not in line]

    cleaned_topics = []
    for line in topics:
        line = line.strip()
        line = str(line)
        if "React Nativ" in line:
            line = line.replace("React Nativ", "React Native")
        if ":" in line:
            line = line.split(":", 1)[1].strip()
        ch_pattern = r"\bCh \d+\s*"
        line = re.sub(ch_pattern, "", line)
        pattern_program = r"Program \d+ .*?"
        line = re.sub(pattern_program, "", line)
        if (
            len(line) > 80
            or is_similar(line)
            or line.isdigit()
            or line.startswith("COMP")
        ):
            line = ""
        cleaned_topics.append(line)

    cleaned_topics = [item for item in cleaned_topics if item != ""]
    cleaned_topics = list(set(cleaned_topics))
    if cleaned_topics == [] or cleaned_topics == ["nan"]:
        return "No Information about Topics"
    else:
        return cleaned_topics


def get_single_course_information(url):
    '''
    Function: get_single_course_information

    This function retrieves information for a single course based on the provided URL.

    Parameters:
    - url (str): The URL of the course page from which information will be scraped.

    Returns:
    - dict: A dictionary containing information about the course, including course description,
    aims, outcomes, schedule, general schedule, year, term, and scraped timestamp.
    '''
    
    raw_scraped_data = scrape_raw_course_data(url)
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
