import logging

from src.lastfm.library.top_tracks import fetch_top_tracks 
from src.lastfm.recommendations.similar_tracks import fetch_similar_tracks
from src.lastfm.library import period
from src.track import Track
from src.lastfm.recommendations.rating_calculator import calculate
from src.lastfm.library.recent_tracks import fetch_recent_tracks


def fetch_recommendations(
          user,
          recommendation_period=period.OVERALL,
          max_similar_tracks_per_top_track=100,
          blacklisted_artists=[],
          prefer_unheard_artists=True):
    """Fetches recommendations for the given user by fetching their top tracks, then getting tracks similar
    to them, and finally filtering out the user's recent tracks"""

    logging.info("Fetching top recommendations for " + user)

    top_tracks = fetch_top_tracks(user=user, a_period=recommendation_period)

    top_tracks_to_recommendations = {}
    recommendations = []
    for top_track in top_tracks:
        try:
            recommendations_for_current_track = fetch_similar_tracks(top_track, max_similar_tracks_per_top_track)
            if recommendations_for_current_track:
                recommendations = recommendations + recommendations_for_current_track
                top_tracks_to_recommendations[top_track] = recommendations_for_current_track
        except Exception as e:
            logging.error(f"Error occurred fetching similar tracks: " + str(e))

    recommendations = calculate(user=user,
                                prefer_unheard_artists=prefer_unheard_artists,
                                top_tracks_to_recommendations=top_tracks_to_recommendations)

    logging.debug(f"Before filtering, fetched " + str(len(recommendations))
                    + " recommendations: " + str(recommendations))

    recommendations = _filter_out_recent_tracks(user, recommendations)

    recommendations = _filter_out_blacklisted_artists(blacklisted_artists, recommendations)

    # Filter out duplicates
    # TODO maybe duplicates should mean a greater chance of getting that recommendation in the playlist?
    recommendations = list(set(recommendations))

    logging.info(f"Fetched " + str(len(recommendations)) + " recommendations: " + str(recommendations))

    return recommendations

def _filter_out_blacklisted_artists(blacklisted_artists, recommendations):
    logging.info("Filtering out blacklisted artists (" + str(blacklisted_artists) + ")...")
    recommendations = [recommendation for recommendation in recommendations
                        if not any(recommendation.artist == blacklisted_artist
                                    for blacklisted_artist in blacklisted_artists)]
    return recommendations

def _filter_out_recent_tracks(user, recommendations):
    recent_tracks = fetch_recent_tracks(user)
    logging.info("Filtering out recent tracks from recommendations...")
    recommendations = [recommendation for recommendation in recommendations
                        if not any(Track.are_equivalent(recommendation, recent_track)
                                    for recent_track in recent_tracks)]
    return recommendations
