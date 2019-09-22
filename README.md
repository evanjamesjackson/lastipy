<h1>Spotify Recommender</h1>
Creates Spotify playlists based on your listening habits by pulling from sources like Last.fm.
<h2>Prerequisites</h2>
Use pip to install:

```
pip install -r spotify_recommender/requirements.txt
```
You will also need a .keys file containing API keys for Last.fm and Spotify:<br/>
https://www.last.fm/api/<br/>
https://developer.spotify.com/documentation/web-api/<br/>
See example.keys for the correct layout.
<h2>Usage</h2>
Run from a command-line like so:

```
python spotify_recommender -f configuration-file 
```
See example.config for an example configuration file.
<h2>Improvements</h2>
* Make a webapp where users can enter their information and have the playlists generated automatically
* Reduce the chance of getting multiple songs from the same artist in a playlist
