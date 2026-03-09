import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_content(user_interest):
    conn = sqlite3.connect("elearning.db")
    df = pd.read_sql("SELECT * FROM courses",conn)

    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(df['skills'])

    user_vec = tfidf.transform([user_interest])
    similarity = cosine_similarity(user_vec,matrix)[0]

    top = similarity.argsort()[-3:][::-1]

    print("\nContent-Based Recommendations:\n")
    for i in top:
        print(df.iloc[i]['title'])

    conn.close()
