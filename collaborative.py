import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_collab(user_id):
    conn = sqlite3.connect("elearning.db")

    activity = pd.read_sql("SELECT * FROM activity",conn)

    if activity.empty:
        print("No activity data yet")
        return

    matrix = activity.pivot_table(index='user_id',columns='course_id',values='rating').fillna(0)

    similarity = cosine_similarity(matrix)

    sim_df = pd.DataFrame(similarity,index=matrix.index,columns=matrix.index)

    similar_users = sim_df[user_id].sort_values(ascending=False)[1:2].index

    rec_courses = activity[activity['user_id'].isin(similar_users)]

    print("\nCollaborative Recommendations:\n")
    print(rec_courses['course_id'].unique())

    conn.close()
