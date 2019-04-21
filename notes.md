~~* Get user's top tracks from Last.fm~~
* For each track, get similar tracks
    * ~~Should be threaded~~
        * No no no no
    * Limit how many similar tracks to get? 
	* Yep easy to do
* Find each similar track in Spotify and add it to playlist
    * How to prevent duplicates across runs?
	* Filter out recent tracks from Last.fm, filter out Spotify library and playlist tracks
* Not really sure which of these steps actually made it runnable in Linux, but it works:
    * Created setup.py and added main.py to scripts section then ran python setup.py develop --user
    * Added #!/usr/env/python to top of main.py
    * Ran chmod +x main.py

