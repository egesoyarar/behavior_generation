# data/context_probabilities.py

# Probabilities for "Place"
PLACE_PROBABILITIES = {
    "Home": 0.4,
    "Outside": 0.1,
    "Cinema": 0.3,
    "Public transportation": 0.05,
    "Workplace": 0.1,
    "Community Center": 0.05
}

# Probabilities for "Day Time"
DAY_TIME_PROBABILITIES = {
    "Morning": 0.1,
    "Afternoon": 0.2,
    "Evening": 0.4,
    "Night": 0.2,
    "Late Night": 0.1
}

# Probabilities for "Day of Week"
DAY_OF_WEEK_PROBABILITIES = {
    "Weekday": 0.6,
    "Weekend": 0.3,
    "Public Holiday": 0.1
}

# Probabilities for "Season"
SEASON_PROBABILITIES = {
    "Summer": 0.2,
    "Spring": 0.2,
    "Winter": 0.35,
    "Fall": 0.25
}

# Probabilities for "With Whom"
COMPANION_PROBABILITIES = {
    "Alone": 0.3,
    "Partner": 0.2,
    "Friends": 0.2,
    "Family": 0.2,
    "Group": 0.1
}
