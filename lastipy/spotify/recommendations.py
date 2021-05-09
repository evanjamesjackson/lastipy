from lastipy.spotify.search import search_for_tracks
from lastipy.recommendations.recommended_track import RecommendedTrack

def fetch_recommendations(spotify, track, max_recommendations_per_track):
    track_in_spotify = search_for_tracks(spotify=spotify, query=track.artist + " " + track.track_name)[0]
    # TODO this accepts up to 5 tracks, so this could be more sophisticated by using multiple top-listened-to tracks in a single call
    recommendations = spotify.recommendations(seed_tracks=[track_in_spotify.spotify_id], limit=max_recommendations_per_track)

    parsed_recommendations = []
    for recommendation in recommendations['tracks']:
        parsed_recommendations.append(RecommendedTrack(track_name=recommendation['name'], artist=recommendation['artists'][0]['name'], spotify_id=recommendation['id'], recommendation_rating=1)) 
    return parsed_recommendations
