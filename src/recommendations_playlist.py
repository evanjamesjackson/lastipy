import logging
import logging.handlers
from src.lastfm import period
from src.lastfm.top_tracks import TopTracksFetcher
from src.lastfm.similar_tracks import SimilarTracksFetcher
from src.lastfm.top_recommendations import TopRecommendationsFetcher
from src.lastfm.recent_tracks import RecentTracksFetcher
from src.lastfm.recent_artists import RecentArtistsFetcher
from src.lastfm.rating_calculator import RatingCalculator
from src.spotify import library, playlist, search
from src.track import Track
from numpy.random import choice


def create_recommendations_playlist(lastfm_user,
                                    spotify_user,
                                    recommendation_period=period.OVERALL,
                                    max_recommendations_per_top_track=50,
                                    playlist_name="Last.fm",
                                    playlist_size=40,
                                    blacklisted_artists=[],
                                    prefer_unheard_artists=True):
    """Creates a playlist for the given Spotify user based on the given Last.fm user's recommendations"""

    recommendations_fetcher = TopRecommendationsFetcher(similar_fetcher=SimilarTracksFetcher(),
                                                        top_fetcher=TopTracksFetcher(),
                                                        recent_fetcher=RecentTracksFetcher(),
                                                        rating_calculator=RatingCalculator())
    recommendations = recommendations_fetcher.fetch(user=lastfm_user,
                                                    recommendation_period=recommendation_period,
                                                    max_similar_tracks_per_top_track=max_recommendations_per_top_track,
                                                    blacklisted_artists=blacklisted_artists,
                                                    prefer_unheard_artists=prefer_unheard_artists)

    saved_tracks = library.get_saved_tracks(spotify_user)
    playlist_tracks = library.get_tracks_in_playlists(spotify_user)

    weights = [recommendation.recommendation_rating for recommendation in recommendations]

    # Potential endless loop here, if no satisfactory track can be found to get the playlist to the given size.
    # This is unlikely to happen though due to the amount of recommendations generated compared to a typical
    # playlist size (eg: 10000 recommendations vs. 40 tracks for a playlist)
    tracks_for_playlist = []
    while len(tracks_for_playlist) < playlist_size:
        recommendation = choice(recommendations, p=weights)

        search_results = search.search_for_tracks(username=spotify_user,
                                                  query=recommendation.artist + " " + recommendation.track_name)
        # Always use the first result, which we can assume is the closest match
        first_result = search_results[0] if search_results else None

        if first_result is not None \
                and Track.are_equivalent(first_result, recommendation) \
                and first_result not in tracks_for_playlist \
                and first_result not in playlist_tracks \
                and first_result not in saved_tracks:
            tracks_for_playlist.append(first_result)

    playlist.add_to_playlist(spotify_user, playlist_name, tracks_for_playlist)

    logging.info("Done!")
