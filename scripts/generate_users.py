import argparse
from behavior_generation.generators.user_generator import generate_users


def main():
    """
    Generate synthetic user data and save it as a CSV file.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic user data.")
    parser.add_argument("--num_users", type=int, default=100, help="Number of users to generate.")
    parser.add_argument("--user_output_file", type=str, default="outputs/users/user_data.csv", help="Output file for user data.")
    args = parser.parse_args()

    num_users = args.num_users
    user_output_file = args.user_output_file
    # Generate user data
    user_df = generate_users(num_users)

    # Format list fields for CSV output
    user_df["liked_genres"] = user_df["liked_genres"].apply(", ".join)
    user_df["disliked_genres"] = user_df["disliked_genres"].apply(", ".join)
    user_df["language_spoken"] = user_df["language_spoken"].apply(", ".join)

    # Save to CSV
    user_df.to_csv(user_output_file, index=False, sep="|", encoding="utf-8")
    print(f"Generated {num_users} users and saved to '{user_output_file}'.")


if __name__ == "__main__":
    main()
