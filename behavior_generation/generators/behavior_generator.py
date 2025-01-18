import random
import pandas as pd
from behavior_generation.data.context_probabilities import (
    LOCATION_PROBS,
    COMPANION_PROBS,
    DAY_OF_WEEK_PROBS,
    SEASON_PROBS,
    TIME_OF_DAY_PROBS,
)
from behavior_generation.utils import pick_from_probabilities


def categorize_duration(duration):
    """
    Categorize movies based on duration.
    """
    if duration < 90:
        return "short"
    elif 90 <= duration <= 120:
        return "medium"
    else:
        return "long"


def categorize_popularity(imdb_rating):
    """
    Categorize movies based on IMDb rating.
    If the rating is NaN, None, or invalid, categorize as 'unpopular'.
    """
    try:
        rating = float(imdb_rating)
        if rating > 7.5:
            return "popular"
        elif rating >= 5:
            return "average"
        else:
            return "unpopular"
    except (ValueError, TypeError):
        return "unpopular"

def generate_behavior_data(users, movies, num_days=30, behaviors_per_day=50):
    """
    Generate synthetic behavior data over multiple days.
    """
    behavior_data = []
    user_records = users.to_dict("records")
    movie_records = movies.to_dict("records")

    for day_number in range(num_days):
        for _ in range(behaviors_per_day):
            user = random.choice(user_records)  # Pick a random user
            movie = random.choice(movie_records)  # Pick a random movie

            # Categorize movie attributes
            duration_category = categorize_duration(movie["duration"])
            popularity_category = categorize_popularity(movie["imdbRating"])

            # Generate context fields
            location = pick_from_probabilities(LOCATION_PROBS)
            companions = pick_from_probabilities(COMPANION_PROBS)
            # season = pick_from_probabilities(SEASON_PROBS)
            day_of_week = pick_from_probabilities(DAY_OF_WEEK_PROBS)
            time_of_day = pick_from_probabilities(TIME_OF_DAY_PROBS)
            user_mood = random.choice(["Happy", "Neutral", "Sad"])  # Example mood generation

            # Append behavior record
            behavior_data.append({
                "day_number": day_number,
                "userId": user["userID"],
                "movieId": movie["movieId"],
                "location": location,
                "companions": companions,
                # "season": season,
                "day_of_week": day_of_week,
                "time_of_movie_watch": time_of_day,
                "user_mood": user_mood,
                "duration_category": duration_category,
                "popularity_category": popularity_category,
            })

    return pd.DataFrame(behavior_data)
