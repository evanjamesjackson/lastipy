import copy


class RatingCalculator:

    def __init__(self, recent_artist_fetcher):
        self.recent_artist_fetcher = recent_artist_fetcher

    def calculate(self, user, top_tracks_to_recommendations, prefer_unheard_artists=True):
        top_tracks_to_recommendations_copy = copy.deepcopy(top_tracks_to_recommendations)

        self._set_ratings_to_playcounts(top_tracks_to_recommendations_copy)

        if prefer_unheard_artists:
            self._adjust_ratings_based_on_recent_artists(top_tracks_to_recommendations_copy, user)

        self._convert_ratings_to_weights(top_tracks_to_recommendations_copy)

        return self._extract_tracks_from_map(top_tracks_to_recommendations_copy)

    def _set_ratings_to_playcounts(self, top_tracks_to_recommendations_copy):
        for top_track in top_tracks_to_recommendations_copy:
            recommendations = top_tracks_to_recommendations_copy[top_track]
            for recommendation in recommendations:
                recommendation.recommendation_rating += top_track.playcount

    def _adjust_ratings_based_on_recent_artists(self, top_tracks_to_recommendations_copy, user):
        recent_artists = self.recent_artist_fetcher.fetch(user)
        for top_track in top_tracks_to_recommendations_copy:
            recommendations = top_tracks_to_recommendations_copy[top_track]
            for recommendation in recommendations:
                for artist in recent_artists:
                    if recommendation.artist == artist.artist_name:
                        recommendation.recommendation_rating = (1 / artist.playcount) * recommendation.recommendation_rating

    def _convert_ratings_to_weights(self, top_tracks_to_recommendations_copy):
        total_ratings = 0
        for top_track in top_tracks_to_recommendations_copy:
            recommendations = top_tracks_to_recommendations_copy[top_track]
            for recommendation in recommendations:
                total_ratings += recommendation.recommendation_rating
        for top_track in top_tracks_to_recommendations_copy:
            recommendations = top_tracks_to_recommendations_copy[top_track]
            for recommendation in recommendations:
                recommendation.recommendation_rating = recommendation.recommendation_rating / total_ratings

    def _extract_tracks_from_map(self, top_tracks_to_recommendations_copy):
        all_recommendations = []
        for top_track in top_tracks_to_recommendations_copy:
            recommendations = top_tracks_to_recommendations_copy[top_track]
            for recommendation in recommendations:
                all_recommendations = all_recommendations + recommendations
        return all_recommendations