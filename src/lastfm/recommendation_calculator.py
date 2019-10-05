def calculate(top_tracks_to_recommendations):
    total_ratings = 0

    for top_track in top_tracks_to_recommendations:
        recommendations = top_tracks_to_recommendations[top_track]
        for recommendation in recommendations:
            recommendation.recommendation_rating += top_track.playcount
            total_ratings += recommendation.recommendation_rating

    for top_track in top_tracks_to_recommendations:
        recommendations = top_tracks_to_recommendations[top_track]
        for recommendation in recommendations:
            recommendation.recommendation_rating = recommendation.recommendation_rating / total_ratings