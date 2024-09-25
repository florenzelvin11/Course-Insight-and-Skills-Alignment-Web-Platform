from models import db, Course, User, UserCode
from flask import Blueprint, request, jsonify, current_app
import pandas as pd
from app import app
import json

db.app = app
app.app_context().push()

df = pd.read_csv("../webscraping/comp_courses_with_skills_and_topics.csv")
for index, row in df.iterrows():
    if row["topics"] == "No Information about Topics":
        row["topics"] = "[]"
    try:
        new_course = Course(
            courseCode=row["Course Code"],
            courseName=row["Course Name"],
            courseDescription=row["Course Description"],
            courseSkills=row["Skills"].replace("'", '"'),
            courseKnowledge=row["Knowledge"].replace("'", '"'),
            topics=row["topics"],
            yearDate=row["Year"],
            term=row["Term"],
            revision=row["Date Scraped"],
            school="School of Computer Science and Engineering",
        )
        print(row["Course Code"])
        db.session.add(new_course)
        db.session.commit()
    except:
        pass
