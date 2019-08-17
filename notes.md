~~* Get user's top tracks from Last.fm~~
~~* For each track, get similar tracks~~
    ~~*Should be threaded~~
        ~~* No no no no~~
    ~~* Limit how many similar tracks to get?~~
    	~~* Built into the API~~
~~* Find each similar track in Spotify and add it to playlist~~
    ~~* How to prevent duplicates across runs?~~
        ~~* Filter out recent tracks from Last.fm, filter out Spotify library and playlist tracks~~
~~* Make it runnable in Linux~~
~~* Schedule on cronjob~~
~~* Make it so that tracks with higher play counts get more representation in recommendations than those with lower counts~~
* "Fast" scrobbler - maybe there's a way to change the amount of time required for a scrobble?
* Not part of this project, but a way to automatically take songs out of library after some time
    * Perhaps after 1 month in library, put into new favorites
    * After 3 months in new favorites, put into old favorites
    * Run every day? Less often?
* Make it a webapp
    * Django?
    * User enters their credentials and saves
        * Maybe also say how often to get a playlist?
    * Would need to show Spotify login then redirect back to my app
