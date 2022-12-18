import speech_recognition as sr
import spotipy
import spotipy.util as util

# Update these to your Spotify account's info, can be grabbed from API
clientID = "client_id_here"
clientSecret = "client_secret_here"
redirectURI = "https://www.google.com"
username = "username_here"

scope = "user-read-private user-read-playback-state user-modify-playback-state"

# Defunct but still working, need to update
token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI)


# Speech recognition initialization
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Listening for command...\n")
    audio = r.listen(source)

# Get transcript
audio = r.recognize_google(audio, show_all='False')['alternative'][0]['transcript'].lower()
print(audio)

# Create a Spotipy client
sp = spotipy.Spotify(auth=token)

# Find device ID
deviceID = sp.devices()['devices'][0]['id']

""" Play a song """
if "play" in audio:
    songName = audio.replace("play", "").strip()
    print("Searching for song: " + songName)

    # search for the song using the recognized command
    results = sp.search(q=songName, type='track')
    tracks = results['tracks']['items']

    # get the first result
    track = tracks[0]

    # get the track's URI
    trackURI = track['uri']

    # start playing the track
    sp.start_playback(device_id=deviceID, uris=[trackURI])
