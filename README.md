
# Behavior Generation for Movie Recommendation Systems

This project generates synthetic datasets for user behavior and satisfaction in movie-watching scenarios. It simulates realistic user profiles and their interactions with movies, considering factors like preferences, contexts, and satisfaction scores.

## Features

- **User Data Generation**:
  - Generates synthetic user profiles with attributes like gender, age range, preferred genres, disliked genres, and languages spoken.
- **Behavior Data Simulation**:
  - Simulates movie-watching behaviors with contextual factors like location, companions, time of day, and seasonality.
  - Assigns a satisfaction score based on multiple weighted factors.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Install dependencies using `pip`:
  ```bash
  pip install -r requirements.txt


### Installation

Install the project as a package, on the root:
```bash
pip install -e .
```

## Usage

### 1. Generate Users
Run the user generation script to create synthetic user profiles:
```bash
python scripts/generate_users.py --num_users 100 --output outputs/users/user_data.csv
```
- **`--num_users`**: Number of users to generate.
- **`--user_output_file`**: Path to save the generated user dataset.

### 2. Generate Behaviors
Run the behavior generation script to simulate movie-watching behaviors:
```bash
python scripts/generate_behaviors.py --num_users 100 --num_days 30 --output outputs/behaviors/behavior_data.csv
```

 
Arguments:

- **`--num_users`**: Number of users to generate. (Default: 100)
- **`--num_days`**: Number of days to simulate. (Default: 30)
- **`--start_date`**: Start date of the simulation in YYYY-MM-DD format. (Default: 2025-01-01)
- **`--user_output_file`**: Path to save the generated user dataset. (Default: outputs/users/user_data.csv)
- **`--behavior_output_file`**: Path to save the generated behavior dataset. (Default: outputs/behaviors/behavior_data.csv)
- **`--movie_data_file`**: Path to the input movie dataset. (Default: behavior_generation/data/movie_data.csv)



### 3. Outputs
- **User Data**: Contains user profiles with attributes like `userId`, `gender`, `age_range`, `liked_genres`, and `language_spoken`.
- **Behavior Data**: Contains contextual behaviors with attributes like `date`, `season`, `day_of_week`, `location`, `companions`, and `satisfaction`.

## Configuration

### Modify Probabilities
Adjust probabilities in the following files to control data distributions:
- **User Attributes**: `behavior_generation/data/user_probabilities.py`
- **Contextual Behaviors**: `behavior_generation/data/context_probabilities.py`

### Satisfaction Scoring
The satisfaction score is calculated using a weighted formula:
```python
satisfaction = (
    (liked_genre_match_score * 0.3) -
    (disliked_genre_match_score * 0.4) +
    (language_match * 0.1) +
    (imdb_rating_normalized * 0.2) +
    (user_mood_score * 0.1) +
    (min(number_of_rewatches, 3) * 0.1)
)
```
Weights and factors can be modified in `calculate_satisfaction_score.py`.

## Output Examples

### Generated User Example
| userId | name        | surname | gender | age_range | lifestyle | country_of_origin | living_country | current_location | liked_genres  | disliked_genres | working_status | marital_status | ethnicity | language_spoken         |
|--------|-------------|---------|--------|-----------|-----------|-------------------|----------------|------------------|---------------|-----------------|----------------|----------------|-----------|-------------------------|
| U0012  | Christopher | Fox     | Female | 35-44     | Active    | Italy             | Italy          | Milan            | ['Crime']     | []              | Student        | Single         | Hispanic  | ['English', 'Italian'] |

### Generated Behavior Example
| day_number | date       | season  | day_of_week | time_of_day | userId | movieId | location | companions | user_mood | satisfaction |
|------------|------------|---------|-------------|-------------|--------|---------|----------|------------|-----------|--------------|
| 11         | 2025-01-12 | Winter  | Sunday      | Night       | U0083  | M03459  | Home     | Partner    | Sad       | 0.48         |



