import argparse
import json
from behavior_generation.generators.user_generator import generate_users


def main():
    """
    Generate synthetic user data and save it as a CSV file.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic user data.")
    parser.add_argument("--num_users", type=int, default=100, help="Number of users to generate.")
    parser.add_argument("--user_output_file", type=str, default="outputs/users/user_data.csv", help="Output file for user data.")
    parser.add_argument("--user_probabilities_file", type=str, default="behavior_generation/data/default_user_probabilities.json", help="Path to user probabilities file.")
    args = parser.parse_args()

    num_users = args.num_users
    user_output_file = args.user_output_file
    user_probabilities_file = args.user_probabilities_file

    try:
        with open(user_probabilities_file, "r", encoding="utf-8") as file:
            user_probabilities = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{user_probabilities_file}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{user_probabilities_file}' contains invalid JSON.")

    # Generate user data
    user_df = generate_users(num_users, user_probabilities)

    # Format list fields for CSV output
    user_df["liked_genres"] = user_df["liked_genres"].apply(", ".join)
    user_df["disliked_genres"] = user_df["disliked_genres"].apply(", ".join)
    user_df["language_spoken"] = user_df["language_spoken"].apply(", ".join)

    # Save to CSV
    user_df.to_csv(user_output_file, index=False, sep="|", encoding="utf-8")
    print(f"Generated {num_users} users and saved to '{user_output_file}'.")


if __name__ == "__main__":
    main()
