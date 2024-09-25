'''
This module provides functions for extracting course topics from various 
sources such as course descriptions, aims, and schedules.
'''

import re
import string
import pandas as pd
import spacy
from fuzzywuzzy import fuzz
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz


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
        "'This is a tentative schedule'",
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
    lines = text.split("\n")
    # Split the text by the '-' character and extract the part after it

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


days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

# Regular expression pattern to match day names (case-insensitive)
day_pattern = r"\b(?:" + "|".join(map(re.escape, days_of_week)) + r")\b"


# Function to remove day names from a text
def remove_days(text):
    """
    Removes days of the week from a given text.

    Parameters:
    - text (str): The input text from which days of the week are to be removed.

    Returns:
    - str: The text with days of the week removed.
    """
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



# Driver code that takes in the comp_courses_with_skills.csv and extracts topics
# Saves this file as comp_courses_with_skills_and_topics.csv
df = pd.read_csv("comp_courses_with_skills.csv")
all_topics = []

for index, row in df.iterrows():
    print(index)
    course = row["Course Code"]
    if course == "COMP9024":
        all_topics.append("No Information about Topics")
        continue
    course_description = row["Course Description"]
    course_aims = row["Course Aims"]
    course_schedule = row["Course Schedule"]
    course_general_schedule = row["Course General Schedule"]

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

    # Define a regular expression pattern to match 'Ch' followed by numbers
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
        if len(line) > 80 or is_similar(line) or line.isdigit():
            line = ""
        cleaned_topics.append(line)

    cleaned_topics = [item for item in cleaned_topics if item != ""]
    cleaned_topics = list(set(cleaned_topics))
    print(cleaned_topics)
    if cleaned_topics == [] or cleaned_topics == ["nan"]:
        all_topics.append("No Information about Topics")
    else:
        all_topics.append(cleaned_topics)


df["topics"] = all_topics
df.to_csv("comp_courses_with_skills_and_topics.csv", index=False)
