##
 #  @filename   :   main.cpp
 #  @brief      :   2.13inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     September 9 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

# Needed for image header 
import epd2in13
import time
import Image
import ImageDraw
import ImageFont
import textwrap

# Needed for Spotify 
import sys
import spotipy
import spotipy.util as util
import time
import os


# Needed to set up
scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = 'astnlucas242@gmail.com'
    #print "Usage: %s username" % (sys.argv[0],)
    #sys.exit()

token = util.prompt_for_user_token(username, scope)

def main():
    # Set up the display parameters 
    epd = epd2in13.EPD()
    epd.init(epd.lut_full_update)

    epd.clear_frame_memory(0xFF)
    epd.display_frame()

    while(True):

        # Check that you have a token before making the call
        if(token == None):
            print "Can't get token for", username
            sys.exit()
            
        # Loop through the spotify results
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print track['name'] + ' - ' + track['artists'][0]['name']
            print track['external_urls']['spotify']

            # Pass in the url to the qr code generator 
            command = "qrencode " + track['external_urls']['spotify'] + " -o qr_code.bmp"          
            os.system(command)

            # clear out the canvas and set up all the font parameters 
            image = Image.new('1', (epd2in13.EPD_WIDTH, epd2in13.EPD_HEIGHT), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
         
            # Doing that cool line wrapping business with the artist name and playlist name
            margin = offset = 120
            for line in textwrap.wrap(track['name'] + ' - ' + track['artists'][0]['name'], width=16):
                print("Broke into: " + line)
                draw.text((10,  offset), line, font = font, fill = 0)
                offset += font.getsize(line)[1]


            # Load the words into memory but don't display yet 
            epd.set_frame_memory(image, 0, 0)
            
            # for partial update -- won't overwrite the words 
            # epd.init(epd.lut_partial_update)

            # Open the image and resize it correctly 
            image = Image.open('qr_code.bmp')
            size = 120,120
            image.thumbnail(size, Image.ANTIALIAS)

            # load and display the e-paper
            epd.set_frame_memory(image, 0, 0)
            epd.display_frame()

            time.sleep(3)

# Should continue forever

if __name__ == '__main__':
    main()
