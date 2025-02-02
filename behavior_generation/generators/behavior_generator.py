import random
import pandas as pd
from datetime import datetime, timedelta

from behavior_generation.utils import pick_from_probabilities

from behavior_generation.generators.satisfaction_calculator import calculate_satisfaction_score

SEASON_BY_MONTH = {
    1: "Winter", 2: "Winter", 3: "Spring",
    4: "Spring", 5: "Spring", 6: "Summer",
    7: "Summer", 8: "Summer", 9: "Autumn",
    10: "Autumn", 11: "Autumn", 12: "Winter"
}

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


def generate_behavior_data(users, movies, user_preferences, num_days=30, start_date="2025-01-01"):
    """
    Generate synthetic behavior data considering seasonality and day_of_week on a per-user basis.
    Each user decides whether to watch a movie each day based on their probabilities,
    with retries based on their watch tendency.
    """
    behavior_data = []
    user_records = users.to_dict("records")
    movie_records = movies.to_dict("records")

    # Create day mapping
    day_mapping = create_day_mapping(start_date, num_days)

    for day_number in range(num_days):
        season = day_mapping[day_number]["season"]
        day_of_week = day_mapping[day_number]["day_of_week"]

        for user in user_records:
            user_id = user["userID"]
            user_watch_tendency = user_preferences[user_id]["WATCH_TENDENCY"]
            user_season_probs = user_preferences[user_id]["SEASON_PROBS"]
            user_day_of_week_probs = user_preferences[user_id]["DAY_OF_WEEK_PROBS"]

            watch_probability = user_season_probs.get(season, 0) * user_day_of_week_probs.get(day_of_week, 0)

            watch_status = False
            for _ in range(user_watch_tendency):
                if random.random() < watch_probability:
                    watch_status = True
                    break

            if watch_status:
                movie = random.choice(movie_records)

                location = pick_from_probabilities(user_preferences[user_id]["LOCATION_PROBS"])
                companions = pick_from_probabilities(user_preferences[user_id]["COMPANION_PROBS"])
                user_mood = random.choice(["Happy", "Neutral", "Sad"])
                time_of_day = pick_from_probabilities(user_preferences[user_id]["TIME_OF_DAY_PROBS"])

                # Calculate satisfaction score
                satisfaction_score = calculate_satisfaction_score(
                    movie["genres"],
                    user["liked_genres"],
                    user["disliked_genres"],
                    movie["language"],
                    user["language_spoken"],
                    movie["imdbRating"],
                    user_mood,
                    movie.get("numberOfRewatches", 0),
                    user["award_hunter"],
                    movie["havingAward"]
                )

                # Add the behavior record
                behavior_data.append({
                    "day_number": day_number,
                    "date": day_mapping[day_number]["date"],
                    "season": season,
                    "day_of_week": day_of_week,
                    "time_of_day": time_of_day,
                    "userId": user_id,
                    "movieId": movie["movieId"],
                    "location": location,
                    "companions": companions,
                    "user_mood": user_mood,
                    "satisfaction_score": satisfaction_score
                })

    return pd.DataFrame(behavior_data)
