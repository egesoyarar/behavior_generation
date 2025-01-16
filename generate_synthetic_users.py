import argparse
import random
import pandas as pd

from person_probabilities import LANGUAGE_PROBS, GENRE_DISLIKE_PROBS


def load_static_data():
    """
    Loads and returns:
      - Lists for clinical genders, age ranges, lifestyles, etc.
      - Mappings for countries -> cities
      - Mappings for countries -> official languages
      - We no longer define the base probabilities here (LANGUAGE_PROBS)
        because we import them from language_probs.py
    """
    clinical_genders = ["Male", "Female", "Other"]
    age_ranges = ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    lifestyles = ["Active", "Sedentary", "Balanced", "Busy", "Relaxed"]

    # Master list of countries
    countries = [
        "Saudi Arabia", "Australia", "Armenia", "Brazil", "Canada", "China",
        "Czech Republic", "Denmark", "Netherlands", "United Kingdom", "Estonia",
        "Philippines", "France", "Germany", "Greece", "Israel", "Hungary",
        "India", "Indonesia", "Italy", "Japan", "South Korea", "Mexico",
        "Norway", "Iran", "Poland", "Portugal", "Romania", "Russia", "Serbia",
        "Spain", "Sweden", "Thailand", "Turkey", "Ukraine", "USA", "Pakistan"
    ]

    cities_by_country = {
        "Saudi Arabia": ["Riyadh"],
        "Australia": ["Sydney", "Melbourne"],
        "Armenia": ["Yerevan"],
        "Brazil": ["Sao Paulo", "Rio de Janeiro"],
        "Canada": ["Toronto", "Montreal"],
        "China": ["Beijing", "Shanghai"],
        "Czech Republic": ["Prague"],
        "Denmark": ["Copenhagen"],
        "Netherlands": ["Amsterdam", "Rotterdam"],
        "United Kingdom": ["London", "Manchester", "Birmingham"],
        "Estonia": ["Tallinn"],
        "Philippines": ["Manila"],
        "France": ["Paris", "Lyon", "Marseille"],
        "Germany": ["Berlin", "Munich", "Frankfurt"],
        "Greece": ["Athens"],
        "Israel": ["Tel Aviv"],
        "Hungary": ["Budapest"],
        "India": ["Mumbai", "Delhi"],
        "Indonesia": ["Jakarta"],
        "Italy": ["Rome", "Milan"],
        "Japan": ["Tokyo", "Osaka", "Kyoto"],
        "South Korea": ["Seoul", "Busan"],
        "Mexico": ["Mexico City"],
        "Norway": ["Oslo"],
        "Iran": ["Tehran"],
        "Poland": ["Warsaw", "Krakow"],
        "Portugal": ["Lisbon", "Porto"],
        "Romania": ["Bucharest"],
        "Russia": ["Moscow", "Saint Petersburg"],
        "Serbia": ["Belgrade"],
        "Spain": ["Madrid", "Barcelona"],
        "Sweden": ["Stockholm"],
        "Thailand": ["Bangkok"],
        "Turkey": ["Istanbul", "Ankara", "Izmir"],
        "Ukraine": ["Kyiv", "Lviv"],
        "USA": ["New York", "Los Angeles", "Chicago"],
        "Pakistan": ["Islamabad"]
    }

    languages_by_country = {
        "Saudi Arabia": ["Arabic"],
        "Australia": ["English"],
        "Armenia": ["Armenian"],
        "Brazil": ["Portuguese"],
        "Canada": ["English", "French"],
        "China": ["Mandarin"],
        "Czech Republic": ["Czech"],
        "Denmark": ["Danish"],
        "Netherlands": ["Dutch"],
        "United Kingdom": ["English"],
        "Estonia": ["Estonian"],
        "Philippines": ["Filipino", "English"],
        "France": ["French"],
        "Germany": ["German"],
        "Greece": ["Greek"],
        "Israel": ["Hebrew"],
        "Hungary": ["Hungarian"],
        "India": ["Hindi", "English"],
        "Indonesia": ["Indonesian"],
        "Italy": ["Italian"],
        "Japan": ["Japanese"],
        "South Korea": ["Korean"],
        "Mexico": ["Spanish"],
        "Norway": ["Norwegian"],
        "Iran": ["Persian"],
        "Poland": ["Polish"],
        "Portugal": ["Portuguese"],
        "Romania": ["Romanian"],
        "Russia": ["Russian"],
        "Serbia": ["Serbian"],
        "Spain": ["Spanish"],
        "Sweden": ["Swedish"],
        "Thailand": ["Thai"],
        "Turkey": ["Turkish"],
        "Ukraine": ["Ukrainian"],
        "USA": ["English"],
        "Pakistan": ["Urdu", "English"]
    }

    all_genres = list(GENRE_DISLIKE_PROBS.keys())
    working_status_options = ["Employed", "Unemployed", "Student", "Retired"]
    marital_status_options = ["Single", "Married", "Divorced", "Widowed"]
    ethnicities = ["Hispanic", "Non-Hispanic White", "Black", "Asian", "Mixed", "Other"]

    return {
        "clinical_genders": clinical_genders,
        "age_ranges": age_ranges,
        "lifestyles": lifestyles,
        "countries": countries,
        "cities_by_country": cities_by_country,
        "languages_by_country": languages_by_country,
        "all_genres": all_genres,
        "working_status_options": working_status_options,
        "marital_status_options": marital_status_options,
        "ethnicities": ethnicities
    }

def pick_living_country(country_of_origin, countries, same_country_prob=0.8):
    """Randomly decide if the user stays in their origin country or moves elsewhere."""
    if random.random() < same_country_prob:
        return country_of_origin
    else:
        return random.choice([c for c in countries if c != country_of_origin])

def pick_city(living_country, cities_by_country):
    """Return a random city from the living_country, or 'Unknown City' if not found."""
    try:
        return random.choice(cities_by_country[living_country])
    except KeyError:
        return "Unknown City"

def pick_disliked_genres():
    """
    For each genre in GENRE_DISLIKE_PROBS, decide if the user dislikes it
    based on a Bernoulli draw with that genre's probability.
    Limit the total disliked genres to a maximum of 3.
    """
    disliked = []
    
    # First, collect all the genres the user would dislike according to probabilities
    for genre, prob in GENRE_DISLIKE_PROBS.items():
        if random.random() < prob:
            disliked.append(genre)
    
    # Then, cap the disliked list at a maximum of 3 genres
    if len(disliked) > 3:
        disliked = random.sample(disliked, 3)
    
    return disliked

def pick_languages(living_country, data_structs, multiplier=2.0):
    """
    - Each language's base probability is in LANGUAGE_PROBS (imported).
    - If a language is official for living_country, multiply its base probability by `multiplier`.
    - Do a random draw for each language to see if the user knows it.
    - Guarantee at least one official language is known.
    """
    languages_by_country = data_structs["languages_by_country"]

    try:
        official_langs = languages_by_country[living_country]
    except KeyError:
        official_langs = ["English"]

    user_langs = []
    for lang, base_prob in LANGUAGE_PROBS.items():
        # Boost probability if it's official
        if lang in official_langs:
            final_prob = min(1.0, base_prob * multiplier)
        else:
            final_prob = base_prob
        
        # Randomly decide if the user knows this language
        if random.random() < final_prob:
            user_langs.append(lang)

    # Guarantee user knows at least one official language
    if not any(lang in official_langs for lang in user_langs):
        user_langs.append(random.choice(official_langs))

    return user_langs

def generate_single_user_record(index, data_structs):
    """Generate one synthetic user record."""
    countries = data_structs["countries"]
    clinical_genders = data_structs["clinical_genders"]
    age_ranges = data_structs["age_ranges"]
    lifestyles = data_structs["lifestyles"]
    all_genres = data_structs["all_genres"]
    working_status_options = data_structs["working_status_options"]
    marital_status_options = data_structs["marital_status_options"]
    ethnicities = data_structs["ethnicities"]
    cities_by_country = data_structs["cities_by_country"]

    user_id = f"U{index+1:04d}"

    clinical_gender = random.choice(clinical_genders)
    age_range = random.choice(age_ranges)
    lifestyle = random.choice(lifestyles)

    country_of_origin = random.choice(countries)
    living_country = pick_living_country(country_of_origin, countries)
    current_location = pick_city(living_country, cities_by_country)

    disliked_genres = pick_disliked_genres()
    current_working_status = random.choice(working_status_options)
    marital_status = random.choice(marital_status_options)
    ethnicity = random.choice(ethnicities)

    # Language logic
    language_spoken = pick_languages(living_country, data_structs, multiplier=2.0)

    return {
        "userID": user_id,
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
        "language_spoken": language_spoken
    }

def generate_synthetic_users(num_users=100):
    """Generate a full DataFrame of synthetic users."""
    data_structs = load_static_data()
    records = []
    for i in range(num_users):
        user_dict = generate_single_user_record(i, data_structs)
        records.append(user_dict)
    return pd.DataFrame(records)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate synthetic movie-watch user dataset.")
    parser.add_argument(
        "--num_users",
        type=int,
        default=100,
        help="Number of users to generate (default: 100)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/synthetic_users.csv",
        help="Output CSV file name (default: synthetic_users.csv)"
    )
    return parser.parse_args()

def main():
    """Main function to handle the script logic."""
    args = parse_args()
    df_users = generate_synthetic_users(num_users=args.num_users)
    
    # Convert list fields to strings for CSV
    df_users["disliked_genres"] = df_users["disliked_genres"].apply(lambda x: ", ".join(x))
    df_users["language_spoken"] = df_users["language_spoken"].apply(lambda x: ", ".join(x))

    # Example of using "|" as a separator instead of comma:
    df_users.to_csv(args.output, index=False, encoding="utf-8", sep="|")
    print(f"Generated {args.num_users} users and saved to '{args.output}'.")

if __name__ == "__main__":
    main()
