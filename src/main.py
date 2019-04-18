import definitions, logging, os
from src.lastfm import period
from src.lastfm.top_tracks import TopTracksFetcher
from src.lastfm.similar_tracks import SimilarTracksFetcher
from src.lastfm.top_recommendations import TopRecommendationsFetcher
from src.lastfm.recent_tracks import RecentTracksFetcher


def main():
    log_file = os.path.join(definitions.ROOT_DIR, ".log")
    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(filename=log_file, mode='w', encoding='utf-8'), logging.StreamHandler()])
    user = 'sonofjack3'
    recommendations_fetcher = TopRecommendationsFetcher(similar_fetcher=SimilarTracksFetcher(),
                                                        top_fetcher=TopTracksFetcher(),
                                                        recent_fetcher=RecentTracksFetcher())
    recommendations_fetcher.fetch(user=user, recommendation_period=period.SEVEN_DAYS, max_similar_tracks_per_top_track=50)


if __name__ == "__main__":
    main()
