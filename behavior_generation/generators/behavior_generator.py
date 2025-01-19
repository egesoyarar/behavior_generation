import random
import pandas as pd
from datetime import datetime, timedelta
from behavior_generation.data.context_probabilities import (
    LOCATION_PROBS,
    COMPANION_PROBS,
    DAY_OF_WEEK_PROBS,
    SEASON_PROBS,
    TIME_OF_DAY_PROBS,
    SEASON_BY_MONTH,
)
from behavior_generation.utils import pick_from_probabilities

from behavior_generation.generators.satisfaction_calculator import calculate_satisfaction_score

def create_day_mapping(start_date, num_days):
    """
    Create a mapping of day_number to season and day_of_week using the start_date.
    """
    day_mapping = {}
    current_date = datetime.strptime(start_date, "%Y-%m-%d")

    for day_number in range(num_days):
        month = current_date.month
        day_of_week = current_date.strftime("%A")
        season = SEASON_BY_MONTH[month]

        day_mapping[day_number] = {
            "date": current_date.strftime("%Y-%m-%d"),
            "day_of_week": day_of_week,
            "season": season
        }
        current_date += timedelta(days=1)  # Move to the next day

    return day_mapping


def distribute_behaviors(total_behaviors, day_mapping):
    """
    Distribute total behaviors across days based on season and day_of_week weights.
    """
    # Calculate weights for each day
    weights = [
        SEASON_PROBS[day_mapping[day]["season"]] *
        DAY_OF_WEEK_PROBS[day_mapping[day]["day_of_week"]]
        for day in range(len(day_mapping))
    ]
    scaling_factor = total_behaviors / sum(weights)

    # Scale weights to match total_behaviors
    distributed_counts = [int(weight * scaling_factor) for weight in weights]

    # Adjust rounding errors to ensure exact total
    while sum(distributed_counts) < total_behaviors:
        distributed_counts[random.randint(0, len(distributed_counts) - 1)] += 1
    while sum(distributed_counts) > total_behaviors:
        distributed_counts[random.randint(0, len(distributed_counts) - 1)] -= 1

    return distributed_counts


def generate_behavior_data(users, movies, num_days=30, total_behaviors=1000, start_date="2025-01-01"):
    """
    Generate synthetic behavior data considering seasonality and day_of_week.
    """
    behavior_data = []
    user_records = users.to_dict("records")
    movie_records = movies.to_dict("records")

    # Create day mapping
    day_mapping = create_day_mapping(start_date, num_days)

    # Distribute behaviors across days based on weights
    behaviors_per_day = distribute_behaviors(total_behaviors, day_mapping)

    for day_number in range(num_days):
        season = day_mapping[day_number]["season"]
        day_of_week = day_mapping[day_number]["day_of_week"]

        for _ in range(behaviors_per_day[day_number]):
            user = random.choice(user_records)
            movie = random.choice(movie_records)

            # Example context fields (location, companions, etc.)
            location = pick_from_probabilities(LOCATION_PROBS)
            companions = pick_from_probabilities(COMPANION_PROBS)
            user_mood = random.choice(["Happy", "Neutral", "Sad"])

            time_of_day = pick_from_probabilities(TIME_OF_DAY_PROBS)


            # Calculate satisfaction score
            satisfaction_score = calculate_satisfaction_score(
                movie["genres"],
                user["liked_genres"],
                user["disliked_genres"],
                movie["language"],
                user["language_spoken"],
                movie["imdbRating"],
                user_mood,
                movie.get("numberOfRewatches", 0)
            )

            # Add season and day_of_week to the behavior record
            behavior_data.append({
                "day_number": day_number,
                "date": day_mapping[day_number]["date"],
                "season": season,
                "day_of_week": day_of_week,
                "time_of_day": time_of_day,
                "userId": user["userID"],
                "movieId": movie["movieId"],
                "location": location,
                "companions": companions,
                "user_mood": user_mood,
                "satisfaction_score": satisfaction_score
            })

    return pd.DataFrame(behavior_data)
