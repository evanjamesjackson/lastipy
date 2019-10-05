
class RatingCalculator:

    def __init__(self, recent_artist_fetcher):
        self.recent_artist_fetcher = recent_artist_fetcher

    def calculate(self, user, top_tracks_to_recommendations):
        for top_track in top_tracks_to_recommendations:
            recommendations = top_tracks_to_recommendations[top_track]
            for recommendation in recommendations:
                recommendation.recommendation_rating += top_track.playcount

        recent_artists = self.recent_artist_fetcher.fetch(user)
        for top_track in top_tracks_to_recommendations:
            recommendations = top_tracks_to_recommendations[top_track]
            for recommendation in recommendations:
                for artist in recent_artists:
                    if recommendation.artist == artist.artist_name:
                        recommendation.recommendation_rating = (1 / artist.playcount) * recommendation.recommendation_rating

        total_ratings = 0
        for top_track in top_tracks_to_recommendations:
            recommendations = top_tracks_to_recommendations[top_track]
            for recommendation in recommendations:
                total_ratings += recommendation.recommendation_rating

        for top_track in top_tracks_to_recommendations:
            recommendations = top_tracks_to_recommendations[top_track]
            for recommendation in recommendations:
                recommendation.recommendation_rating = recommendation.recommendation_rating / total_ratings