# collaborative_based.py
import pandas as pd
from surprise import Reader, Dataset
from sklearn.metrics.pairwise import cosine_similarity  # Add this import
# Remove unused import: import lightgbm as lgb

train = pd.read_csv('resource/data/train.csv')

def prediction_item(item_id, train, model):
    """Map a given favourite movie to users within the
    MovieLens dataset with the same preference.

    Parameters
    ----------
    item_id : int
        A MovieLens Movie ID.
    train : pd.DataFrame
        DataFrame containing user-item ratings.
    model : Surprise model
        Collaborative filtering model.

    Returns
    -------
    list
        User IDs of users with similar high ratings for the given movie.

    """
    reader = Reader(rating_scale=(0, 5))
    load_df = Dataset.load_from_df(train[['userId', 'movieId', 'rating']], reader)
    a_train = load_df.build_full_trainset()

    predictions = []
    for ui in a_train.all_users():
        predictions.append(model.predict(iid=item_id, uid=ui, verbose=False))
    return predictions

def pred_movies(movie_list, train, model):
    """Maps the given favourite movies selected within the app to corresponding
    users within the MovieLens dataset.

    Parameters
    ----------
    movie_list : list
        Three favourite movies selected by the app user.
    train : pd.DataFrame
        DataFrame containing user-item ratings.
    model : Surprise model
        Collaborative filtering model.

    Returns
    -------
    list
        User-ID's of users with similar high ratings for each movie.

    """
    id_store = []
    for i in movie_list:
        predictions = prediction_item(item_id=i, train=train, model=model)
        predictions.sort(key=lambda x: x.est, reverse=True)
        id_store.extend([pred.uid for pred in predictions[:10]])
    return id_store

def collab_model(train, user, top_n=10):
    """Performs Collaborative filtering based upon a list of movies supplied
    by the app user.

    Parameters
    ----------
    train : pd.DataFrame
        DataFrame to be used for collaborative filtering.
    user : int
        User ID for collaborative filtering.
    top_n : int
        Number of top recommendations to return to the user.

    Returns
    -------
    list (str)
        Titles of the top-n movie recommendations to the user.

    """
    indices = pd.Series(train['title'])
    movie_ids = pred_movies([1, 2, 3], train, model=None)  # Placeholder movie IDs [1, 2, 3]
    df_init_users = train[train['userId'].isin(movie_ids)]

    cosine_sim = cosine_similarity(df_init_users[['userId', 'movieId', 'rating']], df_init_users[['userId', 'movieId', 'rating']])
    idx_movies = [indices[indices == i].index[0] for i in [1, 2, 3]]  # Placeholder movie IDs [1, 2, 3]

    rank_movies = [cosine_sim[idx] for idx in idx_movies]
    score_series_movies = [pd.Series(rank).sort_values(ascending=False) for rank in rank_movies]

    listings_movies = pd.concat(score_series_movies).sort_values(ascending=False)
    recommended_movies = list(train['title'][listings_movies.index])

    return recommended_movies[:top_n]
