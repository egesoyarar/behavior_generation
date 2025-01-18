import random


def pick_from_probabilities(prob_dict):
    """
    Select an option based on weighted probabilities.
    """
    options, probabilities = zip(*prob_dict.items())
    return random.choices(options, weights=probabilities, k=1)[0]
