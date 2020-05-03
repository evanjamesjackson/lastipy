
<h1>Lastipy Recommender</h1>
Creates Spotify playlists based on your listening habits by pulling from sources like Last.fm.
<h2>Installation</h2>
Clone the project, navigate to the project directory then use pip to install (will automatically pick up setup.py):

```
pip install .
```
<h2>Usage</h2>
Run from a command-line like so:

```
python lastipy user-configuration-file api-keys-file 
```
See example.config for an example user configuration file.<br/>
You will also need a file containing API keys for Last.fm: https://www.last.fm/api/<br/>
And for Spotify: https://developer.spotify.com/documentation/web-api/<br/>
See example.keys for the correct layout.<br/><br/>
The first time the app is run, the Spotify user will need to give authorization to the application in order to add tracks to a playlist. Once prompted, open the given URL in a browser, log into Spotify, then copy the URL to which you are redirected and paste it into the console. This will only need to be done the first time, since spotipy will cache the authorization.  
<h2>Improvements</h2>

* Make a webapp where users can enter their information and have the playlists generated automatically
