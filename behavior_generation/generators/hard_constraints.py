import random
import pandas as pd

def get_filtered_movies(movies_df):
    """
    Pre-filters movies into separate lists based on constraints.

    :param movies_df: Pandas DataFrame containing movie data.
    :return: Dictionary where keys are constraint types, and values are precomputed lists of movie records.
    """

    filtered_movies = {
        "under_13": movies_df[
            (~movies_df["maturityRating"].isin(["PG-13", "NC-17", "R"]))
        ].to_dict("records"),

        "under_13_with_parent": movies_df[
            (~movies_df["maturityRating"].isin(["NC-17", "R"]))
        ].to_dict("records"),

        "13_17": movies_df[
            (~movies_df["maturityRating"].isin(["NC-17", "R"]))
        ].to_dict("records"),

        "13_17_with_parent": movies_df[
            (~movies_df["maturityRating"].isin(["NC-17"]))
        ].to_dict("records"),

        # Morning should avoid Thriller, or Horror
        "no_morning_thriller_horror": movies_df[
            ~movies_df["genres"].str.contains("Thriller|Horror", regex=True, na=False)
        ].to_dict("records"),

        # Busy people won't watch a movie longer than 2 hours
        "no_long_movie_constraint": movies_df[movies_df["duration"] <= 120].to_dict("records"),

        # Award Hunters will only watch awarded movies
        "strict_award_hunter": movies_df[movies_df["havingAward"] == 1].to_dict("records"),

        # Default (no constraint)
        "no_constraint": movies_df.to_dict("records"),
    }

    return filtered_movies

def pick_movie(movies, user, companions, time_of_day):
    """
    Picks a movie based on the user's constraint.
    """

    if user["hard_constraint"] == "under_13":
        return random.choice(movies["under_13_with_parent"] if companions == "Family" else movies["under_13"])
    
    elif user["hard_constraint"] == "13_17_constraint":
        return random.choice(movies["13_17_with_parent"] if companions == "Family" else movies["13_17"])

    elif user["hard_constraint"] == "no_morning_thriller_horror" and time_of_day == "Morning":
        return random.choice(movies["no_morning_thriller_horror"])

    elif user["hard_constraint"] == "no_long_movie_constraint":
        return random.choice(movies["no_long_movie_constraint"])

    elif user["hard_constraint"] == "strict_award_hunter":
        return random.choice(movies["strict_award_hunter"])

    return random.choice(movies["no_constraint"])
