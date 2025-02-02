import random
import pandas as pd
from faker import Faker
from behavior_generation.data.country_data import (
    COUNTRY_PROBS,
    CITIES_BY_COUNTRY,
    LANGUAGES_BY_COUNTRY,
    LANGUAGE_PROBS_BY_ORIGIN
)
from behavior_generation.data.user_probabilities import (
    GENDER_PROBS,
    AGE_RANGE_PROBS,
    LIFESTYLE_PROBS,
    WORKING_STATUS_PROBS,
    MARITAL_STATUS_PROBS,
    ETHNICITY_PROBS,
    GENRE_LIKE_PROBS,
    GENRE_DISLIKE_PROBS,
    LANGUAGE_PROBS,
)
from behavior_generation.utils import pick_from_probabilities


def generate_single_user(index):
    """
    Generate a single user's data.
    """
    faker = Faker()
    user_id = f"U{index+1:04d}"
    name, surname = faker.first_name(), faker.last_name()

    # Probability-based selections
    clinical_gender = pick_from_probabilities(GENDER_PROBS)
    age_range = pick_from_probabilities(AGE_RANGE_PROBS)
    lifestyle = pick_from_probabilities(LIFESTYLE_PROBS)
    ethnicity = pick_from_probabilities(ETHNICITY_PROBS)

    # Logical selections
    current_working_status = pick_working_status(age_range)
    marital_status = pick_marital_status(age_range)
    country_of_origin = pick_from_probabilities(COUNTRY_PROBS)
    living_country = pick_living_country(country_of_origin)
    current_location = pick_city(living_country)
    liked_genres = pick_liked_genres()
    disliked_genres = pick_disliked_genres(liked_genres)

    language_spoken = pick_languages(living_country, country_of_origin)

    award_hunter = pick_award_hunter()

    return {
        "userID": user_id,
        "name": name,
        "surname": surname,
        "clinical_gender": clinical_gender,
        "age_range": age_range,
        "lifestyle": lifestyle,
        "country_of_origin": country_of_origin,
        "living_country": living_country,
        "current_location": current_location,
        "liked_genres": liked_genres,
        "disliked_genres": disliked_genres,
        "current_working_status": current_working_status,
        "marital_status": marital_status,
        "ethnicity": ethnicity,
        "language_spoken": language_spoken,
        "award_hunter": award_hunter,
    }

def get_specialized_country_probs(origin_country):
    """
    Generate a specialized LANGUAGE_PROBS map for a given origin country,
    updating base LANGUAGE_PROBS with LANGUAGE_PROBS_BY_ORIGIN.

    :param origin_country: The user's origin country.
    :return: A dictionary of updated LANGUAGE_PROBS specific to the origin country.
    """
    if origin_country not in LANGUAGE_PROBS_BY_ORIGIN:
        raise ValueError(f"Country '{origin_country}' not found in LANGUAGE_PROBS_BY_ORIGIN.")

    origin_language_probs = LANGUAGE_PROBS_BY_ORIGIN[origin_country]

    specialized_probs = {
        language: origin_language_probs.get(language, base_prob)
        for language, base_prob in LANGUAGE_PROBS.items()
    }

    return specialized_probs


def generate_users(num_users):
    """
    Generate a DataFrame containing synthetic user data.
    """
    return pd.DataFrame([generate_single_user(i) for i in range(num_users)])


def pick_working_status(age_range):
    """
    Determine the working status based on age range.
    """
    if age_range == "Under 18":
        return "Student"
    if age_range == "65+":
        return "Retired"
    if age_range in ["18-24", "25-34"] and random.random() < 0.5:
        return "Student"
    return pick_from_probabilities(WORKING_STATUS_PROBS)


def pick_marital_status(age_range):
    """
    Determine marital status based on age range.
    """
    return "Single" if age_range == "Under 18" else pick_from_probabilities(MARITAL_STATUS_PROBS)


def pick_living_country(country_of_origin):
    """
    Decide whether the user stays in their origin country or moves elsewhere.
    """
    return random.choices(
        [country_of_origin, random.choice(list(COUNTRY_PROBS.keys()))],
        weights=[0.8, 0.2],
        k=1,
    )[0]


def pick_city(living_country):
    """
    Pick a random city from the given country.
    """
    return random.choice(CITIES_BY_COUNTRY.get(living_country, ["Unknown City"]))


def pick_liked_genres():
    """
    Randomly determine which genres a user likes, capped at 3 genres.
    """
    liked = [genre for genre, prob in GENRE_LIKE_PROBS.items() if random.random() < prob]
    return random.sample(liked, min(len(liked), 3))


def pick_disliked_genres(liked_genres):
    """
    Randomly determine which genres a user dislikes, ensuring no overlap with liked genres,
    capped at 3 genres.
    """
    disliked_candidates = [genre for genre, prob in GENRE_DISLIKE_PROBS.items() if genre not in liked_genres and random.random() < prob]
    return random.sample(disliked_candidates, min(len(disliked_candidates), 3))


def pick_languages(living_country, country_of_origin):
    """
    Determine which languages a user knows, prioritizing official languages of the living country.
    """
    official_langs = LANGUAGES_BY_COUNTRY.get(living_country, ["English"])
    lang_probs = get_specialized_country_probs(country_of_origin)
    user_langs = [
        lang
        for lang, base_prob in lang_probs.items()
        if random.random() < (base_prob * 2.0 if lang in official_langs else base_prob)
    ]
    if not any(lang in official_langs for lang in user_langs):
        user_langs.append(random.choice(official_langs))
    return user_langs

def pick_award_hunter():
    """
    Randomly determine if a user is an award hunter.
    Probability of being an award hunter is 20%.
    :return: 1 if the user is an award hunter, 0 otherwise.
    """
    return 1 if random.random() < 0.2 else 0