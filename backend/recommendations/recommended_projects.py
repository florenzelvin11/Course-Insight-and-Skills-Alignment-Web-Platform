"""
This script provides project recommendations based on student skills and knowledge.

"""

import math

try:
    from similar_words import get_replaceable_words, replace_similar_words_in_dict
except ImportError:
    from recommendations.similar_words import (
        get_replaceable_words,
        replace_similar_words_in_dict,
    )


def cosine_similarity(vector1, vector2):
    """
    Calculate the cosine similarity between two vectors.

    Cosine similarity is a metric that measures the cosine of the angle between two vectors,
    indicating the similarity between them. It ranges from -1 (completely dissimilar) to 1
    (identical), with 0 representing orthogonality.

    Parameters:
        - vector1 (dict): The first vector represented as a dictionary of term-frequency pairs.
        - vector2 (dict): The second vector represented as a dictionary of term-frequency pairs.

    Returns:
        - float: The cosine similarity between the two vectors. The value ranges from -1 to 1,
        with 0 indicating no similarity.
    """
    # Calculate the dot product
    dot_product = sum(
        vector1.get(term, 0) * vector2.get(term, 0)
        for term in set(vector1) | set(vector2)
    )

    # Calculate the magnitude of each vector
    magnitude1 = math.sqrt(sum(value**2 for value in vector1.values()))
    magnitude2 = math.sqrt(sum(value**2 for value in vector2.values()))

    # Calculate the cosine similarity
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0  # Avoid division by zero
    return dot_product / (magnitude1 * magnitude2)


def get_project_recommendations(project_data, student_skills, student_knowledge):
    """
    Generate project recommendations based on student skills and knowledge.

    Parameters:
        - project_data (list): A list of dictionaries representing project data. Each dictionary
        should contain 'name', 'Project required skills', and 'Project required knowledge' keys.
        - student_skills (dict): A dictionary representing the student's skills, where keys are
        terms and values are corresponding skill levels.
        - student_knowledge (dict): A dictionary representing the student's knowledge, where keys
        are terms and values are corresponding knowledge levels.

    Returns:
        - list: A sorted list of project recommendations, each represented as a tuple containing the
        project name and the cosine similarity between the student's combined skills and knowledge
        and the project requirements. The list is sorted from most to least similar projects.
    """

    replace_words = get_replaceable_words(
        project_data, student_skills, student_knowledge
    )
    student_skills_and_knowledge = {
        term: (student_skills.get(term, 0) + student_knowledge.get(term, 0))
        for term in set(student_skills) | set(student_knowledge)
    }
    student_skills_and_knowledge = replace_similar_words_in_dict(
        student_skills_and_knowledge, replace_words
    )

    for project in project_data:
        knwldg = project["Project required knowledge"]
        skills = project["Project required skills"]
        project["Project required knowledge"] = replace_similar_words_in_dict(
            knwldg, replace_words
        )
        project["Project required skills"] = replace_similar_words_in_dict(
            skills, replace_words
        )

    # Calculate the similarity between the student's skills/knowledge and each project
    similarities = []
    for project in project_data:
        project_skills = project["Project required skills"]
        project_knowledge = project["Project required knowledge"]
        project_vector = {
            term: (project_skills.get(term, 0) + project_knowledge.get(term, 0))
            for term in set(project_skills) | set(project_knowledge)
        }

        similarity = cosine_similarity(student_skills_and_knowledge, project_vector)
        similarities.append((project["name"], similarity))

    # Sort projects by similarity (most to least similar)
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities


def get_missing_skills_and_knowledge(
    single_project_data, student_skills, student_knowledge
):
    """
    Identify missing skills and knowledge for a student in the context of a specific project.

    Parameters:
        - single_project_data (list): A list containing a single dictionary representing
        project data. The dictionary should contain 'Project required skills' and 'Project
        required knowledge' keys.
        - student_skills (dict): A dictionary representing the student's skills, where keys
        are terms and values are corresponding skill levels.
        - student_knowledge (dict): A dictionary representing the student's knowledge, where
        keys are terms and values are corresponding knowledge levels.

    Returns:
        - tuple: A tuple containing two sets - the first set represents the missing skills for the
        student regarding the project, and the second set represents the missing knowledge. Both
        sets consist of terms that are required for the project but are not present in the
        student's skills and knowledge.

    """
    knowledge = single_project_data[0]["Project required knowledge"]
    skills = single_project_data[0]["Project required skills"]
    replace_words = get_replaceable_words(
        single_project_data, student_skills, student_knowledge
    )
    knowledge = replace_similar_words_in_dict(knowledge, replace_words)
    skills = replace_similar_words_in_dict(skills, replace_words)
    student_skills = replace_similar_words_in_dict(student_skills, replace_words)
    student_knowledge = replace_similar_words_in_dict(student_knowledge, replace_words)

    set1 = set(knowledge.keys())
    set2 = set(skills.keys())
    set3 = set(student_skills.keys())
    set4 = set(student_knowledge.keys())

    missing_knowledge = set1 - (set3 | set4)

    missing_skills = set2 - (set3 | set4)

    return missing_skills, missing_knowledge


def get_percentage_match(skills_knowledge_size, missing_size):
    """
    Calculate the percentage match based on the sizes of skills and knowledge and the number
    of missing elements.

    Parameters:
        - skills_knowledge_size (int): The total number of elements in the combined set of
        skills and knowledge.
        - missing_size (int): The number of missing elements from the combined set of skills
        and knowledge.

    Returns:
        - int: The percentage match indicating how much of the required skills and knowledge the
        individual possesses.
        The percentage is calculated as (1 - (missing_size / skills_knowledge_size)) * 100 and
        rounded to the nearest integer.

    """
    return round(100 * (1 - missing_size / skills_knowledge_size))
