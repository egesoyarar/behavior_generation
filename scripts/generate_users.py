import pandas as pd
from behavior_generation.generators.user_generator import generate_users


def main():
    """
    Generate synthetic user data and save it as a CSV file.
    """
    num_users = 100  # Number of users to generate
    output_file = "outputs/users/user_data.csv"

    # Generate user data
    user_df = generate_users(num_users)

    # Format list fields for CSV output
    user_df["liked_genres"] = user_df["liked_genres"].apply(", ".join)
    user_df["disliked_genres"] = user_df["disliked_genres"].apply(", ".join)
    user_df["language_spoken"] = user_df["language_spoken"].apply(", ".join)

    # Save to CSV
    user_df.to_csv(output_file, index=False, sep="|", encoding="utf-8")
    print(f"Generated {num_users} users and saved to '{output_file}'.")


if __name__ == "__main__":
    main()
