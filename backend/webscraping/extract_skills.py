'''
This module will extract skills from given text and return those
skills in form of a dictionary where the keys are the skills
and the value is the percentage that this skills holds in 
the list of skills.
'''
# imports
from collections import Counter
import os
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

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
        skill = skill.replace("continue", "").strip()
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


# Driver code to extract all skills and knowledge from a "comp_courses.csv"
# and put those skills and knowledge as a column in the csv
# Output csv is called "comp_courses_with_skills.csv"
# Read the CSV file into a DataFrame
df = pd.read_csv("comp_courses.csv")

# Drop rows with empty 'hello' column
df.dropna(subset=["Course Description"], inplace=True)

decription = df["Course Description"].fillna("")
aim = df["Course Aims"].fillna("")
outline = df["Course Outcomes"].fillna("")
schedule = df["Course Schedule"].fillna("")
general = df["Course General Schedule"].fillna("")

# Create a new column by joining 'hello' and 'goodbye'
df["Combined Course Information"] = (
    decription + " " + aim + " " + outline + " " + schedule + " " + general
)

soft_skills_column = []
hard_skills_column = []

for index, row in df.iterrows():
    course_outline = row["Combined Course Information"]
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

    # Append the cleaned soft and hard skills to the respective lists
    soft_skills_column.append(soft_skills_cleaned)
    hard_skills_column.append(hard_skills_cleaned)


# Add the soft and hard skills columns to the DataFrame
df["Skills"] = soft_skills_column
df["Knowledge"] = hard_skills_column

# Save the DataFrame with the added columns to a new CSV
df.to_csv("comp_courses_with_skills.csv", index=False)
os.remove("output.txt")
