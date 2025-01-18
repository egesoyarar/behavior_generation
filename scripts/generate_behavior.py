import argparse
import pandas as pd
from behavior_generation.generators.behavior_generator import generate_behavior_data
from behavior_generation.generators.user_generator import generate_users


def main():
    """
    Script to generate synthetic behavior data.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate synthetic user and behavior data.")
    parser.add_argument("--num_users", type=int, default=100, help="Number of users to generate.")
    parser.add_argument("--num_days", type=int, default=30, help="Number of days to simulate.")
    parser.add_argument("--behaviors_per_day", type=int, default=50, help="Number of behaviors per day.")
    parser.add_argument("--user_output_file", type=str, default="outputs/users/user_data.csv", help="Output file for user data.")
    parser.add_argument("--behavior_output_file", type=str, default="outputs/behaviors/behavior_data.csv", help="Output file for behavior data.")
    parser.add_argument("--movie_data_file", type=str, default="behavior_generation/data/movie_data.csv", help="Path to movie data file.")
    args = parser.parse_args()

    # Extract arguments
    num_users = args.num_users
    num_days = args.num_days
    behaviors_per_day = args.behaviors_per_day
    user_output_file = args.user_output_file
    behavior_output_file = args.behavior_output_file
    movie_data_file = args.movie_data_file

    print(f"Generating {num_users} users...")
    user_df = generate_users(num_users)
    user_df.to_csv(user_output_file, index=False, sep="|")
    print(f"User data saved to '{user_output_file}'.")

    print("Loading movie data...")
    movie_df = pd.read_csv(movie_data_file, sep="|")

    print(f"Generating behaviors for {num_days} days, {behaviors_per_day} per day...")
    behavior_df = generate_behavior_data(user_df, movie_df, num_days=num_days, behaviors_per_day=behaviors_per_day)
    behavior_df.to_csv(behavior_output_file, index=False, sep="|")
    print(f"Behavior data saved to '{behavior_output_file}'.")


if __name__ == "__main__":
    main()
