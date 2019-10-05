def calculate(top_tracks_to_recommendations):
    for top_track in top_tracks_to_recommendations:
        recommendations = top_tracks_to_recommendations[top_track]
        for recommendation in recommendations:
            recommendation.recommendation_rating = top_track.playcount