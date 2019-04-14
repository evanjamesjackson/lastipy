from lastfm import period
from lastfm.top_tracks import TopTracksFetcher
from lastfm.similar_tracks import SimilarTracksFetcher

def main():
    user = "sonofjack3"
    selected_period = period.SEVEN_DAYS
    max_top_tracks = 50
    max_similar_tracks_per_top_track = 100

    print("Fetching top tracks for user " + user + " over period " + selected_period)
    fetcher = TopTracksFetcher()
    top_tracks = fetcher.fetch_top_tracks(user=user, period=selected_period)
    print(f'Fetched {len(top_tracks)} top tracks')
    print("Top tracks: " + str(top_tracks))

    similar_tracks_fetcher = SimilarTracksFetcher()
    all_similar_tracks = []
    for top_track in top_tracks[:max_top_tracks]:
        try:
            print("Fetching tracks similar to " + str(top_track))
            similar_tracks = similar_tracks_fetcher.fetch_similar_tracks(top_track, max_similar_tracks_per_top_track)
            print("Fetched: " + str(similar_tracks))
            if (similar_tracks):
                all_similar_tracks = all_similar_tracks + similar_tracks
        except Exception as error:
            print(error)
    print(f'Fetched {len(all_similar_tracks)} similar tracks in total')
if __name__ == "__main__":
    main()