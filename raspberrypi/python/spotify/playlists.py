import sys
# Stuff for music
import spotipy
import spotipy.util as util
import json
import progressbar


# Stuff for graphing
from bokeh.plotting import figure, show, output_file
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper
)
from subprocess import call
import os

scope = 'user-library-read, user-read-currently-playing'

# if len(sys.argv) > 1:
#     username = sys.argv[1]

# else:
#     print "Usage: %s username" % (sys.argv[0],)
#     sys.exit()

username = "astnlucas242@gmail.com"

token = util.prompt_for_user_token(username, scope)

url_to_save = ""

# a list of all the qualies to graph
dance = list()
loudness = list()
names = list()

NUM_ITEMS_TO_FETCH = 20

# Make sure you're authenticated
if token:

    # Create a spotify object and grab the last few saved tracks
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks(limit=NUM_ITEMS_TO_FETCH)

    # Make a nice little progress bar to track how this is going because we have to make a call for each song
    bar = progressbar.ProgressBar(max_value=NUM_ITEMS_TO_FETCH)
    index = 1

    # Itterate through each of the tracks that were recently saved and load the audio features
    for item in results['items']:
        track = item['track']

        # Call out to Spotify and ask for this track's audio features
        individual_feature = sp.audio_features(track['id'])

        # Print out a formatted tree of song data
        # print(json.dumps(individual_feature[0]))

        # Store info about the features in the lists to later graph
        dance.append(individu        al_feature[0]['danceability'])
        loudness.append(individual_feature[0]['loudness'])
        names.append(track['name'])

        # Update the progress bar
        bar.update(index)
        index = index + 1


    # Print out the currently playing track just for kicks
    currently_playing = sp.current_user_playing_track()['item']
    print("\nCurrently playing: ")
    print(currently_playing['name'] + " --- " + currently_playing['artists'][0]['name'])

    # Print out the audio features of the currently playing track
    features = sp.audio_features(tracks=sp.current_user_playing_track()['item']['id'])
    print(json.dumps( features, sort_keys=True, indent=3))

    # Print out the arrays we made
    # print(names)
    # print(dance)
    # print(loudness)


    ## Yeah, lets do some fucking gRAPHING DUDE

    # Set up the tools the website will show
    TOOLS = "pan,wheel_zoom,reset,hover,save"

    # Colors
    colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    colors = ['red']

    # Set up the graph itself and set the names
    p = figure(title="Dance vs Loudness", tools=TOOLS)
    p.xaxis.axis_label = 'Dance'
    p.yaxis.axis_label = 'Loudness'


    # Format the data dictionary we load the results from
    #@todo actually, just load this boy up with the calls themselves
    source = ColumnDataSource(data=dict(
        dance = dance,
        loudness = loudness,
        name = names,
    ))

    # Specify how we want each of the datapoints to look
    p.circle('dance', 'loudness', source=source, fill_alpha=0.2, size=10)

    # Set up what hover data we want to show
    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Dance", "@dance"),
        ("Loudness", "@loudness"),
        ("Name", "@name")
    ]

    # Load it!
    output_file("music.html", title="Music analysis example")
    show(p)


else:
    #Whomp, auth failed
    print ("Can't get token for", username)

