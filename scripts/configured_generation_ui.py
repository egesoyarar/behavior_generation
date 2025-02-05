import streamlit as st
import json
import pandas as pd
import datetime
from behavior_generation.generators.user_generator import generate_users
from behavior_generation.generators.preference_generator import generate_multiple_user_preferences
from behavior_generation.generators.behavior_generator import generate_behavior_data

# File path for user probability configurations
USER_PROBABILITIES_FILE = "behavior_generation/data/default_user_probabilities.json"

# **Load existing configuration**
def load_user_probabilities():
    try:
        with open(USER_PROBABILITIES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        st.error(f"Error: The file '{USER_PROBABILITIES_FILE}' is missing or invalid.")
        return {}

user_probabilities = load_user_probabilities()

# **Sidebar: Configurable Settings**
st.sidebar.header("User Generation Settings")
num_users = st.sidebar.number_input("Number of Users", min_value=10, max_value=10000, value=100)
num_days = st.sidebar.number_input("Number of Days", min_value=1, max_value=365, value=30)

# **Adjust probability distributions dynamically**
def adjust_probabilities(category_name):
    st.sidebar.subheader(category_name)
    probs = user_probabilities.get(category_name, {})
    updated_probs = {key: st.sidebar.slider(f"{key}:", 0, 100, int(100*value), 1) for key, value in probs.items()}
    
    # Normalize to sum to 1
    total_prob = sum(updated_probs.values())
    if total_prob > 0:
        updated_probs = {k: v / total_prob for k, v in updated_probs.items()}
    
    return updated_probs

# **Categories of probabilities**
categories = [
    "GENDER_PROBS", "AGE_RANGE_PROBS", "LIFESTYLE_PROBS",
    "WORKING_STATUS_PROBS", "MARITAL_STATUS_PROBS", "ETHNICITY_PROBS"
]
updated_probabilities = {category: adjust_probabilities(category) for category in categories}

# **Run Behavior Generation**
if st.button("Generate Behaviors"):
    st.write("Generating users...")

    # **Step 1: Generate Users**
    user_df = generate_users(num_users, updated_probabilities)
    user_ids = user_df["userID"].tolist()

    # **Step 2: Generate Preferences**
    st.write("Generating user preferences...")
    user_preferences = generate_multiple_user_preferences(user_ids)

    # **Step 3: Generate Behaviors**
    st.write("Generating behavior data...")
    movie_df = pd.read_csv("behavior_generation/data/movie_data.csv", sep="|")
    behavior_df = generate_behavior_data(user_df, movie_df, user_preferences, num_days=num_days)

    # **Save Generated Data**
    user_output_file = "outputs/users/user_data.csv"
    behavior_output_file = "outputs/behaviors/behavior_data.csv"

    user_df.to_csv(user_output_file, index=False, sep="|")
    behavior_df.to_csv(behavior_output_file, index=False, sep="|")

    st.success(f"Users saved to {user_output_file}")
    st.success(f"Behavior data saved to {behavior_output_file}")

    date = datetime.datetime.today().strftime("%d_%m_%Y")
    config_filename = f"behavior_generation/data/user_config_{date}.json"

    # **Save the latest configuration**
    with open(config_filename, "w", encoding="utf-8") as file:
        json.dump(updated_probabilities, file, indent=4)

    # **Show Sample Data**
    st.subheader("Sample User Data")
    st.dataframe(user_df.head())

    st.subheader("Sample Behavior Data")
    st.dataframe(behavior_df.head())

# **Show Current Configurations**
st.subheader("Current Configuration")
config = {"num_users": num_users, "num_days": num_days, **updated_probabilities}
st.json(config)
