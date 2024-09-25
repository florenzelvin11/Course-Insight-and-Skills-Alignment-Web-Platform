"""
Module to provide functions for recommending students based on their profiles.

Usage:
    - Import the module.
    - Use the get_recommended_students function with a dictionary of student profiles
    and a specific student's skills and knowledge as a dict.
"""

from sklearn.metrics.pairwise import cosine_similarity


def get_reccomended_students(student_profiles, z_id):
    """
    Get a list of sorted recommended students based on the cosine similarity of their profiles.

    Parameters:
        - student_profiles (dict): A dictionary containing student IDs as keys and their skills and
        knowledge in a dict as values.
        - zID (str): The student ID for which recommendations are requested.

    Returns:
        - recommended_students (list): A list of recommended student IDs in sorted order from most
        similar to least similar. The remaining students that have no similarity will be returned
        at the end of this list.
    """

    # Calculate cosine similarity between Student1 and other students
    student1_profile = student_profiles[z_id]
    similarities = {}

    for student, profile in student_profiles.items():
        if student != z_id:
            common_features = set(student1_profile.keys()) & set(profile.keys())
            if common_features:
                features1 = [student1_profile[feature] for feature in common_features]
                features2 = [profile[feature] for feature in common_features]
                similarity = cosine_similarity([features1], [features2])[0][0]
                similarities[student] = similarity

    # Sort students by similarity (higher values are more similar)
    recommended_students = sorted(similarities, key=similarities.get, reverse=True)

    # If no similarity, print all other students
    if not recommended_students:
        recommended_students = [
            student for student in student_profiles if student != z_id
        ]

    if len(recommended_students) != len(student_profiles):
        for key in student_profiles.keys():
            if key not in recommended_students and key != z_id:
                recommended_students.append(key)

    return recommended_students
