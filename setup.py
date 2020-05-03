from setuptools import setup, find_packages

setup(name='lastipy',
      version='0.0.1',
      description='Python library that combines Last.fm and Spotify',
      url='http://github.com/evanjamesjackson/lastipy',
      author='Evan Jackson',
      author_email='evanjamesjackson@gmail.com',
      packages=find_packages(),
      entry_points={'console_scripts': [
          'recommendations_playlist = lastipy.recommendations.recommendations_playlist:build_recommendations_playlist'
      ]},
      install_requires=['numpy', 'requests', 'spotipy', 'pytest'])
