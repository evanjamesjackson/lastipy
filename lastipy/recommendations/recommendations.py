import logging

from lastipy.lastfm.library.top_tracks import fetch_top_tracks 
from lastipy.lastfm import lastfm_recommendations
from lastipy.spotify import spotify_recommendations
from lastipy.lastfm.library import period
from lastipy.track import Track
from lastipy.lastfm.library.recent_tracks import fetch_recent_tracks
from lastipy.recommendations.rating_calculator import calculate_ratings


def generate_recommendations(
          user,
          lastfm_api_key,
          spotify,
          recommendation_services='Last.fm',
          recommendation_period=period.OVERALL,
          max_recommendations_per_top_track=100,
          blacklisted_artists=[],
          prefer_unheard_artists=True):
    """Fetches recommendations for the given user by fetching their top tracks, then getting tracks similar
    to them, and filtering out the user's recent tracks and blacklisted artists"""

    logging.info("Fetching recommendations for " + user)

    top_tracks = fetch_top_tracks(user=user, api_key=lastfm_api_key, a_period=recommendation_period)

    top_tracks_to_recommendations = {}
    recommendations = []
    for top_track in top_tracks:
        try:
            recommendations_for_current_track = _fetch_recommendations(recommendation_services, lastfm_api_key, spotify, top_track, max_recommendations_per_top_track) 
            if recommendations_for_current_track:
                recommendations = recommendations + recommendations_for_current_track
                top_tracks_to_recommendations[top_track] = recommendations_for_current_track
        except Exception as e:
            logging.error(f"An error occurred fetching recommendations for track " + str(top_track) + ": " + str(e))

    recommendations = calculate_ratings(user=user,
                                api_key=lastfm_api_key,
                                prefer_unheard_artists=prefer_unheard_artists,
                                top_tracks_to_recommendations=top_tracks_to_recommendations)

    logging.debug(f"Before filtering, fetched " + str(len(recommendations))
                    + " recommendations: " + str(recommendations))

    recommendations = _filter_out_recent_tracks(user, lastfm_api_key, recommendations)

    recommendations = _filter_out_blacklisted_artists(blacklisted_artists, recommendations)

    logging.info("Aftering filtering, fetched " + str(len(recommendations)) + " recommendations")
    logging.debug("Fetched tracks: " + str(recommendations))
    return recommendations

def _filter_out_blacklisted_artists(blacklisted_artists, recommendations):
    logging.info("Filtering out blacklisted artists (" + str(blacklisted_artists) + ")")
    recommendations = [recommendation for recommendation in recommendations
                        if not any(recommendation.artist.lower() == blacklisted_artist.lower()
                                    for blacklisted_artist in blacklisted_artists)]
    return recommendations

def _filter_out_recent_tracks(user, api_key, recommendations):
    recent_tracks = fetch_recent_tracks(user, api_key)
    logging.info("Filtering out recent tracks from recommendations")
    recommendations = [recommendation for recommendation in recommendations
                        if not any(Track.are_equivalent(recommendation, recent_track)
                                    for recent_track in recent_tracks)]
    return recommendations

def _fetch_recommendations(recommendation_services, lastfm_api_key, spotify, track, limit): 
    recommendations = []
    if 'Last.fm' in recommendation_services: 
        recommendations += lastfm_recommendations.fetch_recommendations(api_key=lastfm_api_key, limit=limit, track=track)
    if 'Spotify' in recommendation_services:
        recommendations += spotify_recommendations.fetch_recommendations(spotify=spotify, track=track, limit=limit)
    return recommendations
