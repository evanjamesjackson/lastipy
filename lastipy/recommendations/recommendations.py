import logging

from lastipy.lastfm.library.top_tracks import fetch_top_tracks
from lastipy.lastfm import lastfm_recommendations
from lastipy.spotify import spotify_recommendations
from lastipy.track import Track
from lastipy.lastfm.library.recent_tracks import fetch_recent_tracks
from lastipy.recommendations.rating_calculator import calculate_ratings
from lastipy.spotify import library, search, playlist
from lastipy.lastfm.library import period
from numpy.random import choice


def generate_recommendations(
    lastfm_user,
    lastfm_api_key,
    spotify,
    recommendation_services="Last.fm",
    recommendation_period=period.OVERALL,
    max_recommendations_per_top_track=100,
    blacklisted_artists=[],
    prefer_unheard_artists=True,
):
    """Fetches recommendations for the given user based on their top tracks in Last.fm"""

    logging.info(
        "Fetching recommendations based on " + lastfm_user + "'s top tracks in Last.fm"
    )

    top_tracks = fetch_top_tracks(
        user=lastfm_user, api_key=lastfm_api_key, a_period=recommendation_period
    )

    top_tracks_to_recommendations = {}
    recommendations = []
    for top_track in top_tracks:
        try:
            recommendations_for_current_track = _fetch_recommendations(
                recommendation_services,
                lastfm_api_key,
                spotify,
                top_track,
                max_recommendations_per_top_track,
            )
            if recommendations_for_current_track:
                recommendations = recommendations + recommendations_for_current_track
                top_tracks_to_recommendations[
                    top_track
                ] = recommendations_for_current_track
        except Exception as e:
            logging.error(
                f"An error occurred fetching recommendations for track "
                + str(top_track)
                + ": "
                + str(e)
            )

    recommendations = calculate_ratings(
        user=lastfm_user,
        api_key=lastfm_api_key,
        prefer_unheard_artists=prefer_unheard_artists,
        top_tracks_to_recommendations=top_tracks_to_recommendations,
    )

    logging.debug(
        f"Before filtering, fetched "
        + str(len(recommendations))
        + " recommendations: "
        + str(recommendations)
    )
    recommendations = _filter_out_recent_tracks(
        lastfm_user, lastfm_api_key, recommendations
    )
    recommendations = _filter_out_blacklisted_artists(
        blacklisted_artists, recommendations
    )
    recommendations = _filter_out_saved_tracks(recommendations, spotify)
    recommendations = _filter_out_playlist_tracks(recommendations, spotify)
    recommendations = _filter_out_duplicates(recommendations)
    logging.info(
        "After filtering, fetched " + str(len(recommendations)) + " recommendations"
    )
    logging.debug("Recommendations: " + str(recommendations))

    return recommendations


def _fetch_recommendations(
    recommendation_services, lastfm_api_key, spotify, track, limit
):
    recommendations = []
    if "Last.fm" in recommendation_services:
        recommendations += lastfm_recommendations.fetch_recommendations(
            api_key=lastfm_api_key, limit=limit, track=track
        )
    if "Spotify" in recommendation_services:
        recommendations += spotify_recommendations.fetch_recommendations(
            spotify=spotify, track=track, limit=limit
        )
    return recommendations


def _filter_out_recent_tracks(user, api_key, recommendations):
    recent_tracks = fetch_recent_tracks(user, api_key)
    logging.info("Filtering out recent tracks from recommendations")
    # TODO This is quite slow. Maybe look into using RxPy?
    recommendations = [
        recommendation
        for recommendation in recommendations
        if not any(
            Track.are_equivalent(recommendation, recent_track)
            for recent_track in recent_tracks
        )
    ]
    return recommendations


def _filter_out_blacklisted_artists(blacklisted_artists, recommendations):
    logging.info(
        "Filtering out blacklisted artists ("
        + str(blacklisted_artists)
        + ") from recommendations"
    )
    recommendations = [
        recommendation
        for recommendation in recommendations
        if not any(
            recommendation.artist.lower() == blacklisted_artist.lower()
            for blacklisted_artist in blacklisted_artists
        )
    ]
    return recommendations


# TODO test
def _filter_out_saved_tracks(recommendations, spotify):
    logging.info("Filtering out saved tracks from recommendations")
    saved_tracks = library.get_saved_tracks(spotify)
    recommendations = [
        recommendation
        for recommendation in recommendations
        if not any(
            Track.are_equivalent(recommendation, saved_track)
            for saved_track in saved_tracks
        )
    ]
    return recommendations


# TODO test
def _filter_out_playlist_tracks(recommendations, spotify):
    logging.info("Filtering out tracks in the user's playlists")
    playlist_tracks = playlist.get_tracks_in_playlists(spotify)
    recommendations = [
        recommendation
        for recommendation in recommendations
        if not any(
            Track.are_equivalent(recommendation, playlist_track)
            for playlist_track in playlist_tracks
        )
    ]
    return recommendations


# TODO test
def _filter_out_duplicates(recommendations):
    logging.info("Filtering out duplicates")
    logging.debug(str(len(recommendations)) + " tracks before removing duplicates")
    tracks_without_duplicates = []
    # We remove duplicates with a list comprehension rather than the traditional hack of using a set, since that
    # requires the object to be hashable; plus we only want to compare the track name/artist of each track, not
    # any of the other fields (eg: Spotify ID) which might in fact differ
    [
        tracks_without_duplicates.append(track_x)
        for track_x in recommendations
        if not any(
            Track.are_equivalent(track_x, track_y)
            for track_y in tracks_without_duplicates
        )
    ]
    logging.debug(str(len(recommendations)) + " tracks after removing duplicates")
    return tracks_without_duplicates
