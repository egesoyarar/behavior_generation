import argparse
import pandas as pd
import json
from behavior_generation.generators.behavior_generator import generate_behavior_data
from behavior_generation.generators.user_generator import generate_users
from behavior_generation.generators.preference_generator import generate_multiple_user_preferences


def main():
    """
    Script to generate synthetic behavior data.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic user and behavior data.")
    parser.add_argument("--num_users", type=int, default=100, help="Number of users to generate.")
    parser.add_argument("--num_days", type=int, default=30, help="Number of days to simulate.")
    parser.add_argument("--start_date", type=str, default="2025-01-01", help="Start date of simulation.")
    parser.add_argument("--user_output_file", type=str, default="outputs/users/user_data.csv", help="Output file for user data.")
    parser.add_argument("--preference_output_file", type=str, default="outputs/users/preferences.json", help="Output file for preference probabilities.")
    parser.add_argument("--behavior_output_file", type=str, default="outputs/behaviors/behavior_data.csv", help="Output file for behavior data.")
    parser.add_argument("--movie_data_file", type=str, default="behavior_generation/data/movie_data.csv", help="Path to movie data file.")
    parser.add_argument("--user_probabilities_file", type=str, default="behavior_generation/data/default_user_probabilities.json", help="Path to user probabilities file.")
    args = parser.parse_args()

    num_users = args.num_users
    num_days = args.num_days
    start_date= args.start_date
    user_output_file = args.user_output_file
    preference_output_file = args.preference_output_file
    behavior_output_file = args.behavior_output_file
    movie_data_file = args.movie_data_file
    user_probabilities_file = args.user_probabilities_file

    try:
        with open(user_probabilities_file, "r", encoding="utf-8") as file:
            user_probabilities = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{user_probabilities_file}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{user_probabilities_file}' contains invalid JSON.")

    print(user_probabilities)

    print(f"Generating {num_users} users...")
    user_df = generate_users(num_users, user_probabilities)
    user_df.to_csv(user_output_file, index=False, sep="|")
    print(f"User data saved to '{user_output_file}'.")

    user_preferences = generate_multiple_user_preferences(user_df["userID"])
    with open(preference_output_file, "w", encoding="utf-8") as f:
        json.dump(user_preferences, f, indent=4)
    print(f"Preference data saved to '{preference_output_file}'.")

    print("Loading movie data...")
    movie_df = pd.read_csv(movie_data_file, sep="|")

    print(f"Generating behaviors for {num_days} days")
    behavior_df = generate_behavior_data(
        user_df,
        movie_df,
        user_preferences,
        num_days=num_days,
        start_date=start_date
    )
    behavior_df.to_csv(behavior_output_file, index=False, sep="|")
    print(f"Behavior data saved to '{behavior_output_file}'.")


if __name__ == "__main__":
    main()
