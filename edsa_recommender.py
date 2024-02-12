# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
merged_df = pd.read_csv('resources/data/merged_data.csv')  # Make sure to adjust the path accordingly
title_list = load_movie_titles('resources/data/merged_data.csv')

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System", "Solution Overview", "Meet the Team", "Contact Details"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png', use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('First Option', title_list[14930:15200])
        movie_2 = st.selectbox('Second Option', title_list[25055:25255])
        movie_3 = st.selectbox('Third Option', title_list[21100:21200])
        fav_movies = [movie_1, movie_2, movie_3]

        # Correct indexing
        i = merged_df[merged_df['title'].isin(fav_movies)].index[0]
        movie_titles = merged_df.loc[i, 'title']

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies, top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i + 1) + '. ' + j)
                except:
                    st.error("Oops! Looks like this algorithm doesn't work. We'll need to fix it!")

        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                user_id = st.number_input("Enter your user ID:")
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(df=merged_df, user_id=user_id, movie_list=fav_movies, top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i + 1) + '. ' + j)
                except:
                    st.error("Oops! Looks like this algorithm doesn't work. We'll need to fix it.")

    # -------------------------------------------------------------------
    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("""
        Welcome to Cinemate - your personalized movie recommendation engine!
        
        Cinemate uses advanced algorithms to provide you with movie recommendations based on your preferences.
        Whether you're a fan of content-based filtering or collaborative-based filtering, Cinemate has you covered.
        
        Simply select your favorite movies, choose an algorithm, and let Cinemate crunch the numbers to suggest
        movies tailored just for you. Enjoy the movie-watching experience with Cinemate Recommender!
        """)

    elif page_selection == "Meet the Team":
        # Team Lead
        st.write("- Ayanda Moloi: Team Lead")
        st.write("  - Background: Leadership and Project Management")
        st.write("  - Experience: Led the overall project development and coordination of this project.")

        # Project Manager
        st.write("- Cathrine Mamosadi: Project Manager")
        st.write("  - Background: Project Management and Coordination")
        st.write("  - Experience: Managed project timelines, resources, and communication.")

        # Data Engineer
        st.write("- Sakhile Zungu: Data Engineer")
        st.write("  - Background: Data Engineering and Database Management")
        st.write("  - Experience: Responsible for Model training and engineering.")

        # Data Scientist
        st.write("- Pinky Ndleve: Data Scientist")
        st.write("  - Background: Data Science and Machine Learning")
        st.write("  - Experience: Developed machine learning models and conducted data analysis.")

        # App Developer
        st.write("- Lauretta Maluleke: App Developer")
        st.write("  - Background:  Web Development")
        st.write("  - Experience: Developed the Streamlit web application for Recommender systems.")

        # Data Analyst
        st.write("- Asmaa Hassan: Data Analyst")
        st.write("  - Background: Data visualization and Analysis")
        st.write("  - Experience: Power Bi and Python analysis.")

    # Contact details
    elif page_selection == "Contact Details":
        st.write("Send us an email at info@CineMate.co.za")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.

if __name__ == '__main__':
    main()
