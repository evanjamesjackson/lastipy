from setuptools import setup, find_packages

setup(name='spotify_recommender',
      version='1.0',
      description='Creates Spotify playlists based on your listening habits by pulling from sources like Last.fm.',
      url='http://github.com/evanjamesjackson/spotify_recommender',
      author='Evan Jackson',
      author_email='evanjamesjackson@gmail.com',
      packages=find_packages(where='src'),
      install_requires=['numpy', 'requests', 'spotipy', 'pytest'])