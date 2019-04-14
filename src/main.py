from .lastfm import period
from .lastfm.top_recommendations import TopRecommendationsFetcher

def main():
    TopRecommendationsFetcher().fetch(user='sonofjack3', recommendation_period=period.ONE_MONTH)

if __name__ == "__main__":
    main()