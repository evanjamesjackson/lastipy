import definitions, logging, os
from src.lastfm import period
from src.lastfm.top_recommendations import TopRecommendationsFetcher
from src.lastfm.recent_tracks import RecentTracksFetcher


def main():
    log_file = os.path.join(definitions.ROOT_DIR, "spotify_recommender.log")
    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(filename=log_file, mode='w', encoding='utf-8'), logging.StreamHandler()])
    user = 'sonofjack3'
    recommendations = TopRecommendationsFetcher().fetch(user=user, recommendation_period=period.SEVEN_DAYS)
    recent_tracks = RecentTracksFetcher().fetch(user=user)
    # recommendations = [track for track in recommendations if track not in recent_tracks]
    # print(str(recommendations))
    # print(len(recommendations))


if __name__ == "__main__":
    main()
