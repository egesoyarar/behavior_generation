def calculate_satisfaction_score(
    movie_genres,
    liked_genres,
    disliked_genres,
    movie_language,
    user_languages,
    imdb_rating,
    user_mood,
    number_of_rewatches
):
    """
    Calculate the satisfaction score as a weighted composite of various factors.

    :param movie_genres: String of genres of the movie (comma-separated).
    :param liked_genres: List of genres the user likes.
    :param disliked_genres: List of genres the user dislikes.
    :param movie_language: String of the movie's languages (comma-separated).
    :param user_languages: List of the user's known languages.
    :param imdb_rating: IMDb rating of the movie (0 to 10).
    :param user_mood: User's mood during the movie ("Happy", "Neutral", "Sad").
    :param number_of_rewatches: Number of times the user has rewatched the movie.
    :return: Satisfaction score (0 to 1).
    """
    # Convert string inputs to lists
    movie_genres = movie_genres.split(", ") if isinstance(movie_genres, str) else movie_genres
    movie_languages = movie_language.split(", ") if isinstance(movie_language, str) else movie_language

    # Calculate genre match score
    def calculate_genre_match_score(movie_genres, genres):
        if not movie_genres or not genres:
            return 0
        match_count = len(set(movie_genres).intersection(set(genres)))
        return match_count / len(movie_genres)

    # Calculate user mood score
    def calculate_user_mood_score(user_mood):
        USER_MOOD_SCORES = {
            "Happy": 1.0,
            "Neutral": 0.7,
            "Sad": 0.4,
        }
        return USER_MOOD_SCORES.get(user_mood, 0.7)

    # Genre match score
    liked_genre_match_score = calculate_genre_match_score(movie_genres, liked_genres)
    disliked_genre_match_score = calculate_genre_match_score(movie_genres, disliked_genres)

    # Language match
    language_match = 1 if any(lang in user_languages for lang in movie_languages) else 0

    # Normalize IMDb rating to 0-1 scale
    imdb_rating_normalized = float(imdb_rating) / 10 if imdb_rating else 0

    # User mood score
    user_mood_score = calculate_user_mood_score(user_mood)

    # Calculate the weighted satisfaction score
    satisfaction = (
        (liked_genre_match_score * 0.3) -
        (disliked_genre_match_score * 0.4) +
        (language_match * 0.1) +
        (imdb_rating_normalized * 0.2) +
        (user_mood_score * 0.1) +
        (min(number_of_rewatches, 3) * 0.1)  # Cap rewatch influence
    )

    return round(max(0, min(satisfaction, 1)), 2)