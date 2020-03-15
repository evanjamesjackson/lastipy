from setuptools import setup

setup(name='spotify_recommender',
      version='1.0',
      description='Creates Spotify playlists based on your listening habits by pulling from sources like Last.fm.',
      url='http://github.com/evanjamesjackson/spotify_recommender',
      author='Evan Jackson',
      author_email='evanjamesjackson@gmail.com',
      install_requires=['numpy', 'requests', 'spotipy', 'pytest'])