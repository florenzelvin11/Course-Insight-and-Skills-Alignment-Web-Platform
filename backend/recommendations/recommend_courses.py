"""
This script provides course recommendations based on student skills and knowledge.

"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def combine_skills_and_knowledge(courses_data):
    """
    Parameters: List of dicts (courses_data) containing courses' name, skills and knowledge
    as seperate fields in a dict

    Returns: List of dicts with each dict containing two fields: course_name and
    skills_and_knowledge_covered
    """
    courses = []

    # Create a combined dictionary of skills and knowledge with weighted values for each course
    for course_data in courses_data:
        course_name = course_data["name"]
        course_knowledge = course_data["knowledge"]
        course_skills = course_data["skills"]
        course_skills_and_knowledge = {
            term: (course_knowledge.get(term, 0) + course_skills.get(term, 0))
            for term in set(course_knowledge) | set(course_skills)
        }
        courses.append(
            {
                "course_name": course_name,
                "skills_and_knowledge_covered": course_skills_and_knowledge,
            }
        )

    return courses


def get_recommended_courses(student_skills_and_knowledge, courses_data):
    """
    Parameters:
    1. Dict of student_skills_and_knowledge
    2. List of dicts (courses_data) containing courses' name, skills and knowledge
    as seperate fields in a dict

    Returns: Sorted courses based on cosine similarity in descending order (most recommended first)

    """
    courses = combine_skills_and_knowledge(courses_data)

    # Fit the TF-IDF vectorizer on all the combined data
    all_text_data = [
        " ".join(course["skills_and_knowledge_covered"].keys()) for course in courses
    ]
    tfidf = TfidfVectorizer()
    tfidf.fit(all_text_data)

    # Calculate cosine similarity between student skills and each course's skills
    cosine_sims = []
    student_skills_text = " ".join(student_skills_and_knowledge.keys())

    for course in courses:
        course_skills_text = " ".join(course["skills_and_knowledge_covered"].keys())
        skills_matrix = tfidf.transform([student_skills_text, course_skills_text])
        cosine_sim = linear_kernel(skills_matrix[0:1], skills_matrix[1:2])
        cosine_sims.append(cosine_sim[0][0])

    recommended_courses = {}
    for i, course in enumerate(courses):
        course_name = course["course_name"]
        cosine_sim = cosine_sims[i]
        recommended_courses[course_name] = cosine_sim

    # Sort courses based on cosine similarity in descending order (most recommended first)
    sorted_courses = sorted(
        recommended_courses.items(), key=lambda x: x[1], reverse=True
    )

    return sorted_courses
