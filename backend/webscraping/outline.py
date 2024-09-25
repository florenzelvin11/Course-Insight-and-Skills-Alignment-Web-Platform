'''
Web Scraper for UNSW Course Information

This script uses Selenium, a web scraping library, to extract course information
from the UNSW course outline website. It navigates through the website, collects
data such as course description, aims, outcomes, schedule, and general topics,
and saves the information into a CSV file for data cleaning and NLP. 

'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")
# optional
chrome_options.add_argument("--no-sandbox")
# optional
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
# load website
YEAR = "2023"
TERM = "T3"
FORMATS = ["In%20Person", "Multimodal"]


headings = [
    "Course Code",
    "Course Name",
    "Type",
    "Course Description",
    "Course Aims",
    "Course Outcomes",
    "Course Schedule",
    "Course General Schedule",
    "Year",
    "Term",
    "Date Scraped",
]

with open("comp_courses.csv", "r", newline="") as csvfile:
    csv_reader = csv.reader(csvfile)

    csv_list = [row for row in csv_reader]

csv_list = csv_list[1:]
csv_list.insert(0, headings)


for row in csv_list[1:]:
    COURSE = row[0]
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # optional
    chrome_options.add_argument("--no-sandbox")
    # optional
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    for FORMAT in FORMATS:
        url = f"https://www.unsw.edu.au/course-outlines/course-outline#year={YEAR}&term=Term%203&deliveryMode={FORMAT}&deliveryFormat=Standard&teachingPeriod={TERM}&deliveryLocation=Kensington&courseCode={COURSE}&activityGroupId=1"
        driver.get(url)

        try:
            button = driver.find_element(
                By.XPATH,
                "/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/button",
            )
            button.click()
        except Exception as e:
            continue
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

        def get_single_paragraph(path):
            try:
                paragraph_element = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, path))
                )
                paragraph_text = paragraph_element.text
                return paragraph_text
            except Exception as e:
                pass

        course_description = [item for item in course_description if item != ""]

        if len(course_description) == 0:
            paragraph_xpath = "/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[4]/div/div/span/div/div/div[3]/span/div/div/p"
            paragraph = get_single_paragraph(paragraph_xpath)
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
            paragraph = get_single_paragraph(paragraph_xpath)
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
            paragraph = get_single_paragraph(paragraph_xpath)
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
            break

        button_topics = driver.find_element(
            By.XPATH,
            "/html/body/div[4]/div/div[4]/div/div[1]/div/div[3]/span/div/ul/li[8]/button",
        )
        button_topics.click()

        # Course Schedule
        number = 1
        topics = []
        consecutive_exceptions = 0  # Initialize the consecutive exceptions counter
        max_consecutive_exceptions = (
            5  # Set the maximum consecutive exceptions threshold
        )

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
                consecutive_exceptions += (
                    1  # Increment the consecutive exceptions counter
                )
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
            break

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        row.append(course_description)
        row.append(course_aims)
        row.append(course_outcomes)
        row.append(course_schedule)
        row.append(course_general_schedule)
        row.append(YEAR)
        row.append(TERM)
        row.append(formatted_datetime)
        print(row)
    driver.quit()


with open("comp_courses.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(csv_list)
