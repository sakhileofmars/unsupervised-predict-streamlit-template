

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np
import pickle
# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model
from sklearn.feature_extraction.text import TfidfVectorizer #for vectorizing text data'
from sklearn.preprocessing import StandardScaler #for numeri values
from sklearn.decomposition import TruncatedSVD # for collaborative model


# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')
merged_df = pd.read_csv(r'C:\Users\MALULEKE LOUIS\Downloads\merged data.csv')
# Loading the vectorizer using pickle
with open('resources/models/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)
#LOADING THE SCALER
with open('resources/models/scaler.pkl', 'rb') as scaling:
    scaler = pickle.load(scaling)
    # loading model
with open('resources/models/svd_model.pkl', 'rb') as model:
    SVD = pickle.load(model)  
# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview", "Meet the Team"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
		    movies = pd.read_csv('resources/data/movies.csv')
                try:
                    with st.spinner('Crunching the numbers...'):
			    model = 'SVD'
			    merged_df['predict_score'] = merged_df.apply(lambda row: collab_model.predict_score(row['userId'], row['title']), axis=1)

                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    # Set the dark background color
if page_selection == "Solution Overview":
    st.title("Solution Overview")
    st.write("Describe your winning approach on this page")

# Meet the team page
elif page_selection == 'Meet the Team':
    st.title("Meet the Team")

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
    st.write("  - Experience: Power Bi and Python analysis")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
