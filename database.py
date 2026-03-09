import sqlite3

conn = sqlite3.connect("elearning.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
name TEXT,
interest TEXT
)
""")

# Courses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses(
id INTEGER PRIMARY KEY,
title TEXT,
skills TEXT
)
""")

# Activity table
cursor.execute("""
CREATE TABLE IF NOT EXISTS activity(
user_id INTEGER,
course_id INTEGER,
rating INTEGER
)
""")

# Insert sample courses
courses = [
(1,"Python Basics","python programming beginner"),
(2,"Machine Learning","machine learning python ai"),
(3,"Data Science","data analysis python statistics"),
(4,"Web Development","html css javascript web"),
(5,"Deep Learning","neural networks ai python")
]

cursor.executemany("INSERT OR IGNORE INTO courses VALUES(?,?,?)",courses)

conn.commit()
conn.close()
print("Database created")
