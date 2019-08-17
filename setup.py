from setuptools import setup, find_packages

setup(
    name='spotify_recommender',
    version='1.0',
    description='creates spotify playlists based on your listening habits, by pulling from sources like last.fm',
    author='evan jackson',
    author_email='evanjamesjackson@gmail.com',
    packages=find_packages(),
    scripts='spotify_recommender/recommendations_playlist.py',
    install_requires=['numpy', 'requests', 'spotipy']
)
