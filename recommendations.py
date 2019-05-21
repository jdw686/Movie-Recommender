"""This is a placeholder for the docstring of the recommender program"""
import math
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from sqlalchemy import create_engine


def get_recommendations(user_movies, user_rating):
    """This is a placeholder for the docstring of the get_recommendation function."""
    # below initializes the sql table used for the movie ratings
    movies_db = create_engine('postgres://localhost:5431/jdw686', echo=True)
    ratings = pd.read_sql_table('rating_table', movies_db)
    ratings = pd.pivot_table(ratings, values='rating', index=['userid'], columns=['title'])
    ratings.fillna(0.0, inplace=True)

    movie_titles = list(ratings.columns)
    user_input = [(process.extract(user_movies[0], movie_titles)[0][0], float(user_rating[0])),
                  (process.extract(user_movies[1], movie_titles)[0][0], float(user_rating[1])),
                  (process.extract(user_movies[2], movie_titles)[0][0], float(user_rating[2]))]

    user_input = dict(user_input)

    new_user = []
    for movie in ratings.columns:
        if movie in user_input:
            rating_input = user_input[movie]
        else:
            rating_input = 0.0
        new_user.append(rating_input)

    new_user = np.array(new_user)

    def cosim(input1, input2):
        num = np.dot(input1, input2)
        xnorm = math.sqrt(sum(input1 ** 2))
        ynorm = math.sqrt(sum(input2 ** 2))
        denom = xnorm * ynorm
        return num / denom

    value_list = []
    for user in ratings.index:
        value = cosim(new_user, ratings.loc[user])
        value_list.append(value)

    df_value = pd.DataFrame(data=value_list, index=ratings.index, columns=['cosine'])
    df_value.sort_values(by='cosine', ascending=False, inplace=True)
    top_selection = df_value.index[0]

    recommendation = ratings.loc[top_selection].sort_values(ascending=False)
    recommendation = pd.DataFrame(recommendation)
    recommendation = recommendation.reset_index()
    locator = np.random.randint(0, len(recommendation[recommendation[top_selection] == 5.0]))

    return list(recommendation[recommendation.index == locator]['title'])[0]
