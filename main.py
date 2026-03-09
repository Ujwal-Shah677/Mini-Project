import sqlite3
import database
from content_based import recommend_content
from collaborative import recommend_collab

conn = sqlite3.connect("elearning.db")
cursor = conn.cursor()

# Add sample user
name = input("Enter name: ")
interest = input("Enter interest: ")

cursor.execute("INSERT INTO users(name,interest) VALUES(?,?)",(name,interest))
user_id = cursor.lastrowid

# Add activity (use explicit column names)
cursor.execute("INSERT INTO activity(user_id,course_id,rating) VALUES(?,?,?)",(user_id,1,5))
cursor.execute("INSERT INTO activity(user_id,course_id,rating) VALUES(?,?,?)",(user_id,2,4))

conn.commit()
conn.close()

recommend_content(interest)
recommend_collab(user_id)
