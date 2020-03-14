
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
python spotify_recommender configuration-file 
```
See example.config for an example configuration file.<br/><br/>
The first time the app is run, the Spotify user will need to give authorization to the application in order to add tracks to a playlist. Once prompted, open the URL in a browser, log into Spotify, then copy the URL to which you are redirected and paste it into the console. This will only need to be done the first time, since spotipy will cache the authorization.  
<h2>Improvements</h2>

* Make a webapp where users can enter their information and have the playlists generated automatically
* Figure out how to use venv properly and set up a Jenkins autobuilder so I don't have to log into the Amazon instance every time I change something
