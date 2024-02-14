# content_based.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def data_preprocessing(df, subset_size):
    """Prepare data for use within Content filtering algorithm.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be preprocessed.
    subset_size : int
        Number of movies to use within the algorithm.

    Returns
    -------
    Pandas Dataframe
        Subset of movies selected for content-based filtering.

    """
    # Split genre data into individual words.
    df['keyWords'] = df['genres'].str.replace('|', ' ')

    # Entire dataset
    subset_size = int(len(df))
    df_subset = df[:subset_size]

    # Return the subset
    return df_subset

def content_model(df, title, top_n=10):
    """Performs Content filtering based upon a list of movies supplied
       by the app user.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be used for content-based filtering.
    title : str
        Movie title chosen by the app user.
    top_n : int
        Number of top recommendations to return to the user.

    Returns
    -------
    list (str)
        Titles of the top-n movie recommendations to the user.

    """
    # Initializing the empty list of recommended movies
    recommended_movies = []
    
    # Data preprocessing
    data = data_preprocessing(df, 27000)

    # Instantiating and generating the count matrix
    count_vec = CountVectorizer()
    count_matrix = count_vec.fit_transform(data['keyWords'])
    indices = pd.Series(data['title'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # Getting the index of the movie that matches the title
    idx_movie = indices[indices == title].index[0]

    # Creating a Series with the similarity scores in descending order
    rank_movie = cosine_sim[idx_movie]
    score_series_movie = pd.Series(rank_movie).sort_values(ascending=False)

    # Getting the indexes of the top_n most similar movies
    listings_movie = score_series_movie.append(score_series_movie).sort_values(ascending=False)

    # Store movie names
    recommended_movies = []

    # Appending the names of movies
    top_50_indexes = list(listings_movie.iloc[1:50].index)

    # Removing chosen movie
    top_indexes = np.setdiff1d(top_50_indexes, [idx_movie])

    for i in top_indexes[:top_n]:
        recommended_movies.append(list(df['title'])[i])

    return recommended_movies