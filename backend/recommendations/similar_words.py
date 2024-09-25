"""
Functions for processing and analyzing textual data, including word similarity,
common word identification, and replacement of similar words.
"""

import spacy

nlp = spacy.load("en_core_web_lg")


def calculate_similarity(phrase1, phrase2):
    """
    Calculate the semantic similarity between two phrases using spaCy word vectors.

    Parameters:
        - phrase1 (str): The first input phrase for which similarity is to be calculated.
        - phrase2 (str): The second input phrase for which similarity is to be calculated.

    Returns:
        - float: A similarity score ranging from 0.0 to 1.0, where 0.0 indicates no similarity,
        and 1.0 indicates identical phrases.

    Note:
        - The function uses spaCy's pre-trained word vectors to capture semantic information.
        - If either of the input phrases lacks word vectors, the function returns 0.0.
    """
    doc1 = nlp(phrase1)
    doc2 = nlp(phrase2)

    if doc1.has_vector and doc2.has_vector:
        return doc1.similarity(doc2)
    return 0.0


def has_common_word(phrase1, phrase2):
    """
    Check if two phrases contain at least one common word.

    Parameters:
        - phrase1 (str): The first input phrase to be compared.
        - phrase2 (str): The second input phrase to be compared.

    Returns:
        - bool: True if there is at least one common word between the two phrases,
        otherwise False.
    """
    words1 = phrase1.split()
    words2 = phrase2.split()

    # Check if both phrases contain the same word
    common_words = set(words1).intersection(words2)

    return bool(common_words)


def replace_similar_words_in_dict(input_dict, keywords):
    """
    Replace words in a dictionary with similar words based on semantic similarity.

    Parameters:
        - input_dict (dict): The input dictionary where words are to be replaced. Keys represent
        original terms, and values represent corresponding values.
        - keywords (list): A list of potential replacement words to consider. These replacement
        words are expected to be semantically similar to the original terms in the input dictionary.

    Returns:
        - dict: A new dictionary where keys are updated based on semantic similarity to the
        provided keywords. Values are aggregated for keys that have been replaced with the
        same keyword.

    """

    updated_dict = {}
    for key, value in input_dict.items():
        updated_key = key  # Initialize updated_key with the original key
        for keyword in keywords:
            similarity = calculate_similarity(key, keyword)
            if similarity > 0.8:
                updated_key = keyword
                break

        # Combine values if the updated_key already exists in the updated_dict
        if updated_key in updated_dict:
            updated_dict[updated_key] += value
        else:
            updated_dict[updated_key] = value

    return updated_dict


def join_data(project_data, student_skills, student_knowledge):
    """
    Combine and extract unique terms from project data, student skills, and student knowledge.

    Parameters:
        - project_data (list): A list of dictionaries representing project data. Each dictionary
        should contain 'Project required skills' and 'Project required knowledge' keys.
        - student_skills (dict): A dictionary representing the student's skills, where keys are
        terms and values are corresponding skill levels.
        - student_knowledge (dict): A dictionary representing the student's knowledge, where keys
        are terms and values are corresponding knowledge levels.

    Returns:
        - list: A list containing unique terms extracted from project data, student skills,
        and student knowledge. The list represents the combined set of skills and knowledge.
    """

    student_skills_and_knowledge = {
        term: (student_skills.get(term, 0) + student_knowledge.get(term, 0))
        for term in set(student_skills) | set(student_knowledge)
    }
    all_skills_and_knowledge = []

    for project in project_data:
        knowledge = project["Project required knowledge"]
        skills = project["Project required skills"]
        all_skills_and_knowledge.extend(list(knowledge.keys()))
        all_skills_and_knowledge.extend(list(skills.keys()))

    all_skills_and_knowledge.extend(list(student_skills_and_knowledge.keys()))
    all_words = list(set(all_skills_and_knowledge))
    return all_words


def check_duplicates_in_replace_words(replace_words, word1, remove_dups):
    """
    Check for and handle duplicates in a list of replaceable words based on semantic similarity.

    Parameters:
        - replace_words (list): A list of words identified as replaceable based on semantic
        similarity.
        - word1 (str): The word being considered for replacement.
        - remove_dups (list): A list containing words to be removed as duplicates.

    Returns:
        - list: An updated list of words to be removed as duplicates. This list is modified based
        on the semantic similarity between 'word1' and existing words in 'replace_words'.

    """

    for word in replace_words:
        similarity2 = calculate_similarity(word, word1)
        if similarity2 > 0.8:
            if len(word) > len(word1):
                remove_dups.append(word)
            else:
                remove_dups.append(word1)
    return remove_dups


def get_replaceable_words(project_data, student_skills=None, student_knowledge=None):
    """
    Identify and return a list of replaceable words from a given dataset, considering semantic
    similarity.

    Parameters:
        - project_data (list): A list of dictionaries representing project data. Each dictionary
        should contain 'Project required skills' and 'Project required knowledge' keys.
        - student_skills (dict, optional): A dictionary representing the student's skills, where
        keys are terms and values are corresponding skill levels. Default is None.
        - student_knowledge (dict, optional): A dictionary representing the student's
        knowledge, where keys are terms and values are corresponding knowledge levels.
        Default is None.

    Returns:
        - list: A list of words identified as potentially replaceable based on semantic similarity.
        These words are selected from the combined set of terms present in project data,
        student skills, and student knowledge.

    """

    if not student_skills is None and not student_knowledge is None:
        all_words = join_data(project_data, student_skills, student_knowledge)
    else:
        all_words = project_data

    replace_words = []
    remove_dups = []

    for word1 in all_words:
        for word2 in all_words:
            similarity = calculate_similarity(word1, word2)
            if word1 != word2:
                if (
                    similarity > 0.8
                    and word1 not in replace_words
                    and word2 not in replace_words
                    and has_common_word(word1, word2)
                ):
                    remove_dups = check_duplicates_in_replace_words(
                        replace_words, word1, remove_dups
                    )
                    replace_words.append(word1)

    replace_words = [word for word in replace_words if word not in remove_dups]

    return replace_words
