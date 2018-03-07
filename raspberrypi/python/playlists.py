import sys
import spotipy
import spotipy.util as util
from subprocess import call
import os

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

url_to_save = ""

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print track['name'] + ' - ' + track['artists'][0]['name']
        print track['href']

        command = "qrencode " + track['external_urls']['spotify'] + " -o qr_code.bmp"

        print command
        
        os.system(command)


        
else:
    print "Can't get token for", username

