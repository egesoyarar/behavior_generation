import argparse
import random
import pandas as pd
from faker import Faker
from user_probabilities import (
    LANGUAGE_PROBS,
    GENRE_DISLIKE_PROBS,
    GENDER_PROBS,
    AGE_RANGE_PROBS,
    LIFESTYLE_PROBS,
    WORKING_STATUS_PROBS,
    MARITAL_STATUS_PROBS,
    ETHNICITY_PROBS,
)
from country_data import COUNTRY_PROBS, CITIES_BY_COUNTRY, LANGUAGES_BY_COUNTRY


def pick_from_probabilities(prob_dict):
    """
    Select an option based on weighted probabilities.
    :param prob_dict: Dictionary with options and their probabilities
    :return: Selected option
    """
    options, probabilities = zip(*prob_dict.items())
    return random.choices(options, weights=probabilities, k=1)[0]


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


def pick_languages(living_country, multiplier=2.0):
    """
    Determine which languages a user knows, prioritizing official languages of the living country.
    """
    official_langs = LANGUAGES_BY_COUNTRY.get(living_country, ["English"])
    user_langs = [
        lang
        for lang, base_prob in LANGUAGE_PROBS.items()
        if random.random() < (base_prob * multiplier if lang in official_langs else base_prob)
    ]
    if not any(lang in official_langs for lang in user_langs):
        user_langs.append(random.choice(official_langs))
    return user_langs


def generate_names():
    """
    Generate random first and last names using the Faker library.
    """
    faker = Faker()
    return faker.first_name(), faker.last_name()


def generate_single_user(index):
    """
    Generate a single user's data.
    """
    user_id = f"U{index+1:04d}"
    name, surname = generate_names()

    # Probability-based selections
    clinical_gender = pick_from_probabilities(GENDER_PROBS)
    age_range = pick_from_probabilities(AGE_RANGE_PROBS)
    lifestyle = pick_from_probabilities(LIFESTYLE_PROBS)
    ethnicity = pick_from_probabilities(ETHNICITY_PROBS)

    # Logical selections
    current_working_status = pick_working_status(age_range)
    marital_status = pick_marital_status(age_range)
    country_of_origin = pick_from_probabilities(COUNTRY_PROBS)
    living_country = random.choices(
        [country_of_origin, random.choice(list(COUNTRY_PROBS.keys()))],
        weights=[0.8, 0.2],
        k=1
    )[0]
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
    return pd.DataFrame([generate_single_user(i) for i in range(num_users)])


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic user data.")
    parser.add_argument("--num_users", type=int, default=100, help="Number of users to generate (default: 100)")
    parser.add_argument("--output", type=str, default="outputs/user_data.csv", help="Output CSV file (default: user_data.csv)")
    return parser.parse_args()


def main():
    """
    Main script to generate synthetic user data and save it to a CSV file.
    """
    args = parse_arguments()
    user_df = generate_users(args.num_users)

    # Convert list fields to string format for CSV output
    user_df["disliked_genres"] = user_df["disliked_genres"].apply(", ".join)
    user_df["language_spoken"] = user_df["language_spoken"].apply(", ".join)

    # Save the dataset
    user_df.to_csv(args.output, index=False, sep="|", encoding="utf-8")
    print(f"Generated {args.num_users} users and saved to '{args.output}'.")


if __name__ == "__main__":
    main()
