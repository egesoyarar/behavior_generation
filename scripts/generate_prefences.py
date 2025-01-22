import argparse
import json
from behavior_generation.generators.preference_generator import generate_multiple_user_preferences


def main():
    """
    Generate synthetic user preferences and save them as a JSON file.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic user preferences.")
    parser.add_argument("--num_users", type=int, default=100, help="Number of users to generate preferences for.")
    parser.add_argument("--preference_output_file", type=str, default="outputs/users/preferences.json", help="Output file for preferences.")
    args = parser.parse_args()

    num_users = args.num_users
    preference_output_file = args.preference_output_file

    # Generate user IDs
    user_ids = [f"U{str(i + 1).zfill(4)}" for i in range(num_users)]

    # Generate preferences for all users
    preferences = generate_multiple_user_preferences(user_ids)

    # Save preferences to JSON file
    with open(preference_output_file, "w", encoding="utf-8") as f:
        json.dump(preferences, f, indent=4)

    print(f"Generated preferences for {num_users} users and saved to '{preference_output_file}'.")


if __name__ == "__main__":
    main()
