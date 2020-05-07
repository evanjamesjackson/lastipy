from setuptools import setup, find_packages

setup(name='lastipy',
      version='1.0.8',
      description='Python library that combines Last.fm and Spotify',
      url='http://github.com/evanjamesjackson/lastipy',
      author='Evan Jackson',
      author_email='evanjamesjackson@gmail.com',
      packages=find_packages(),
      entry_points={'console_scripts': [
          'recommendations_playlist = scripts.recommendations_playlist.__main__:main',
          'save_new_releases = scripts.save_new_releases.__main__:main'
      ]},
      install_requires=['numpy', 'requests', 'spotipy', 'pytest'])
