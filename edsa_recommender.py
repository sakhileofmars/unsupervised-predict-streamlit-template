"""
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
import streamlit as st
import pandas as pd  # Add this import statement
from recommenders.content_based import content_model
from recommenders.collaborative_based import collab_model
from utils.data_loader import load_movie_titles

title_list = load_movie_titles('resources/data/movies.csv')
train = pd.read_csv('resources/data/train.csv')

def main():
    page_options = ["Recommender System", "Solution Overview", "Movie Search", "Meet the Team", "Contact Details"]
    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
    
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png', use_column_width=True)

        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        if sys == 'Content Based Filtering':
            st.write('### Enter Your Three Favorite Movies')
            movie_1 = st.selectbox('First Option', title_list[14930:15200])
            movie_2 = st.selectbox('Second Option', title_list[25055:25255])
            movie_3 = st.selectbox('Third Option', title_list[21100:21200])
            fav_movies = [movie_1, movie_2, movie_3]

            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(train, title=fav_movies[0], top_n=10)
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
                        top_recommendations = collab_model(train, user=user_id, top_n=10)
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i + 1) + '. ' + j)
                except:
                    st.error("Oops! Looks like this algorithm doesn't work. We'll need to fix it.")
    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------

    elif page_selection == "Solution Overview":
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
        st.write("  - Experience: Power Bi and Python analysis")

    elif page_selection == "Contact Details":
        st.title("Contact Details")
        st.write("""
        For any inquiries or assistance, please feel free to reach out to us:

        - Email: contact@cinemate.com
        - Phone: +27 (31) 456-7890

        We value your feedback and are here to help you with any questions you may have.
        """)

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.

    st.write("\n\n\n")  # Adding some space before the Thank You message
    st.markdown("**Thank you for using Cinemate Recommender!**")

if __name__ == '__main__':
    main()
