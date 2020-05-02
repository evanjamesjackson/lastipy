from setuptools import setup, find_packages

setup(name='lastipy_recommender',
      version='0.0.2',
      description='Creates Spotify playlists based on your listening habits by pulling from sources like Last.fm.',
      url='http://github.com/evanjamesjackson/lastipy_recommender',
      author='Evan Jackson',
      author_email='evanjamesjackson@gmail.com',
      packages=find_packages(),
      entry_points={'console_scripts': [
          'lastipy_recommender = lastipy_recommender.__main__:main'
      ]},
      install_requires=['lastipy', 'numpy', 'requests', 'spotipy', 'pytest'])
