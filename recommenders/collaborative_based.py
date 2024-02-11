# Script dependencies
import pandas as pd
import numpy as np
import pickle
from surprise import Reader, Dataset
from sklearn.metrics.pairwise import cosine_similarity
import lightgbm as lgb  # Added import for LightGBM

# Importing data
movies_df = pd.read_csv('resources/data/movies.csv', sep=',')
ratings_df = pd.read_csv('resources/data/ratings.csv')
merged_df = pd.read_csv('resources/data/merged_data.csv')

# We make use of an lgbm model trained on a subset of the MovieLens 10k dataset.
model = pickle.load(open('resources/models/lgbm_model.pkl', 'rb'))

def prediction_item(item_id):
    """Map a given favourite movie to users within the
    MovieLens dataset with the same preference.

    Parameters
    ----------
    item_id : int
        A MovieLens Movie ID.

    Returns
    -------
    list
        User IDs of users with similar high ratings for the given movie.

    """
    # Data preprocessing
    # Assuming 'userId', 'movieId', and 'rating' are columns in merged_df
    reader = Reader(rating_scale=(0, 5))
    load_df = Dataset.load_from_df(merged_df[['userId', 'movieId', 'rating']], reader)
    a_train = load_df.build_full_trainset()

    predictions = []
    for ui in a_train.all_users():
        predictions.append(model.predict(iid=item_id, uid=ui, verbose=False))
    return predictions

def pred_movies(movie_list):
    """Maps the given favourite movies selected within the app to corresponding
    users within the MovieLens dataset.

    Parameters
    ----------
    movie_list : list
        Three favourite movies selected by the app user.

    Returns
    -------
    list
        User-ID's of users with similar high ratings for each movie.

    """
    # Store the id of users
    id_store = []
    # For each movie selected by a user of the app,
    # predict a corresponding user within the dataset with the highest rating
    for i in movie_list:
        predictions = prediction_item(item_id=i)
        predictions.sort(key=lambda x: x.est, reverse=True)
        # Take the top 10 user id's from each movie with the highest rankings
        for pred in predictions[:10]:
            id_store.append(pred.uid)
    # Return a list of user id's
    return id_store

# !! DO NOT CHANGE THIS FUNCTION SIGNATURE !!
# You are, however, encouraged to change its content.
def collab_model(movie_list, top_n=10):
    """Performs Collaborative filtering based upon a list of movies supplied
    by the app user.

    Parameters
    ----------
    movie_list : list (str)
        Favorite movies chosen by the app user.
    top_n : type
        Number of top recommendations to return to the user.

    Returns
    -------
    list (str)
        Titles of the top-n movie recommendations to the user.

    """

    indices = pd.Series(merged_df['title'])
    movie_ids = pred_movies(movie_list)
    df_init_users = merged_df[merged_df['userId'] == movie_ids[0]]
    for i in movie_ids:
        df_init_users = df_init_users.append(merged_df[merged_df['userId'] == i])
    # Getting the cosine similarity matrix
    cosine_sim = cosine_similarity(np.array(df_init_users), np.array(df_init_users))
    idx_1 = indices[indices == movie_list[0]].index[0]
    idx_2 = indices[indices == movie_list[1]].index[0]
    idx_3 = indices[indices == movie_list[2]].index[0]
    # Creating a Series with the similarity scores in descending order
    rank_1 = cosine_sim[idx_1]
    rank_2 = cosine_sim[idx_2]
    rank_3 = cosine_sim[idx_3]
    # Calculating the scores
    score_series_1 = pd.Series(rank_1).sort_values(ascending=False)
    score_series_2 = pd.Series(rank_2).sort_values(ascending=False)
    score_series_3 = pd.Series(rank_3).sort_values(ascending=False)
    # Appending the names of movies
    listings = score_series_1.append(score_series_1).append(score_series_3).sort_values(ascending=False)
    recommended_movies = []
    # Choose top 50
    top_50_indexes = list(listings.iloc[1:50].index)
    # Removing chosen movies
    top_indexes = np.setdiff1d(top_50_indexes, [idx_1, idx_2, idx_3])
    for i in top_indexes[:top_n]:
        recommended_movies.append(list(movies_df['title'])[i])
    return recommended_movies
