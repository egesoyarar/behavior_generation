import random
import math
from decimal import Decimal, ROUND_DOWN

from behavior_generation.data.preference_categories import (
    COMPANIONS,
    SEASONS,
    DAYS_OF_WEEK,
    TIMES_OF_DAY,
    LOCATIONS,
)


def normalize_probabilities(probabilities):
    """
    Normalize a dictionary of probabilities so that their sum equals 1
    and round each probability to 2 decimal places using Decimal for precision.
    """
    total = sum(probabilities.values())
    normalized = {key: Decimal(value / total) for key, value in probabilities.items()}
    rounded = {key: normalized[key].quantize(Decimal('0.01'), rounding=ROUND_DOWN) for key in normalized}
    rounded_total = sum(rounded.values())

    if rounded_total != Decimal('1.00'):
        diff = Decimal('1.00') - rounded_total
        max_key = max(rounded, key=rounded.get)
        rounded[max_key] += diff

    return {key: float(value) for key, value in rounded.items()}

def generate_normal_probabilities(categories):
    """
    Generate independent probabilities for seasons (do not normalize).
    """
    return {category: round(random.random(), 2) for category in categories}

def generate_dominant_probabilities(categories):
    """
    Generate probabilities with one category being dominant.
    
    :param categories: List of categories (e.g., COMPANIONS, SEASONS).
    :return: A dictionary of normalized probabilities.
    """
    dominant_index = random.randint(0, len(categories) - 1)
    base_weights = [1.0 if i == dominant_index else random.uniform(0.1, 0.5) for i in range(len(categories))]
    probabilities = {category: weight for category, weight in zip(categories, base_weights)}
    return normalize_probabilities(probabilities)


def generate_single_user_preferences(user_id):
    """
    Generate user-specific probabilities for companions, seasons, days of the week,
    times of the day, and locations.

    :param user_id: Unique identifier for the user.
    :return: A dictionary containing user-specific probabilities for different contexts.
    """

    watch_tendency_probs = round(random.random(), 2)
    companion_probs = generate_dominant_probabilities(COMPANIONS)
    season_probs = generate_normal_probabilities(SEASONS)
    day_of_week_probs = generate_normal_probabilities(DAYS_OF_WEEK)
    time_of_day_probs = generate_dominant_probabilities(TIMES_OF_DAY)
    location_probs = generate_dominant_probabilities(LOCATIONS)

    return {
        user_id: {
            "WATCH_TENDENCY_PROBS": watch_tendency_probs,
            "COMPANION_PROBS": companion_probs,
            "SEASON_PROBS": season_probs,
            "DAY_OF_WEEK_PROBS": day_of_week_probs,
            "TIME_OF_DAY_PROBS": time_of_day_probs,
            "LOCATION_PROBS": location_probs,
        }
    }

def generate_multiple_user_preferences(user_ids):
    """
    Generate user-specific probabilities for a list of user IDs.

    :param user_ids: List of user IDs.
    :return: A dictionary with user IDs as keys and their respective preferences as values.
    """
    all_preferences = {}
    for user_id in user_ids:
        all_preferences.update(generate_single_user_preferences(user_id))
    return all_preferences