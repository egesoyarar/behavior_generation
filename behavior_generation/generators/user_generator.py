import random
from faker import Faker
from behavior_generation.data.country_data import (
    COUNTRY_PROBS,
    CITIES_BY_COUNTRY,
    LANGUAGES_BY_COUNTRY,
)
from behavior_generation.data.user_probabilities import (
    GENDER_PROBS,
    AGE_RANGE_PROBS,
    LIFESTYLE_PROBS,
    WORKING_STATUS_PROBS,
    MARITAL_STATUS_PROBS,
    ETHNICITY_PROBS,
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
    disliked_genres = pick_disliked_genres()
    language_spoken = pick_languages(living_country)

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
        "disliked_genres": disliked_genres,
        "current_working_status": current_working_status,
        "marital_status": marital_status,
        "ethnicity": ethnicity,
        "language_spoken": language_spoken,
    }


def generate_users(num_users):
    """
    Generate a DataFrame containing synthetic user data.
    """
    import pandas as pd

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


def pick_disliked_genres():
    """
    Randomly determine which genres a user dislikes, capped at 3 genres.
    """
    disliked = [genre for genre, prob in GENRE_DISLIKE_PROBS.items() if random.random() < prob]
    return random.sample(disliked, min(len(disliked), 3))


def pick_languages(living_country):
    """
    Determine which languages a user knows, prioritizing official languages of the living country.
    """
    official_langs = LANGUAGES_BY_COUNTRY.get(living_country, ["English"])
    user_langs = [
        lang
        for lang, base_prob in LANGUAGE_PROBS.items()
        if random.random() < (base_prob * 2.0 if lang in official_langs else base_prob)
    ]
    if not any(lang in official_langs for lang in user_langs):
        user_langs.append(random.choice(official_langs))
    return user_langs
