# !/usr/bin/python3
import sys
import os

import logging
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import subprocess
import numpy as np
from datetime import datetime as d

# include -t in arguments to switch to testing
testing = "-t" in sys.argv

if not testing:
    try:
        from waveshare_epd import epd7in5
    except:
        testing = True
        print("epd7in5 not found, switching to test mode (no epd)")

def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T-o.T) + o.T).T)


# --- Update tide information
# Determines whether the clock hand is moving towards high or low tide and calculates the time left
# Then feeds this info to draw()
def update():
    now = d.now()
    # High/Low tide info from tide output
    output = subprocess.run(["tide","-l",location,"-b",now.strftime("%Y-%m-%d %H:%M"),"-m","n"],shell=False, capture_output=True).stdout
    output = output.decode("utf-8").split('\n')[1:3] # obtains 2nd and 3rd lines which should always be H/L tides
    e1 = output[0]
    e2 = output[1]
    time1 = d.strptime(output[0][3:26],"%Y-%m-%d %I:%M %p %Z")
    # time2 = d.strptime(output[1][3:26],"%Y-%m-%d %I:%M %p %Z")
    minutesUntilEvent = (time1 - now).total_seconds() / 60
    tideMinutes = 745 - minutesUntilEvent if e1[0] == 'H' else 372.5 - minutesUntilEvent
    draw(tideMinutes, e1[3:], e2[3:])

# --- Draw on PNG or EDP
def draw(tideMinutes, hText, lText):
    if not testing: 
        epd.Clear()

    rotation = tideMinutes*rotationMin
    # Create a Vertical image
    logging.info("Drawing on the Vertical image...")
    dimensions = (384, 640) if testing else (epd.height, epd.width)
    tideClock = Image.new('1', dimensions, 255)  # 255: clear the frame

    # Load clock dial bitmap
    ClockDial = Image.open('clock.bmp')
    tideClock.paste(ClockDial, (0, 0))

    draw = ImageDraw.Draw(tideClock)
    # Border
    draw.rectangle((0, 0, 383, 639), outline=(0))
    # Set rotation for hand
    ClockHandRotation = rotate(points, origin=origin, degrees=rotation)
    # Draw Hand
    draw.polygon((tuple([tuple(row) for row in ClockHandRotation])), fill=(0))
    # Draw center circle
    draw.ellipse(xy=(182, 182, 202, 202), fill=(0))
    draw.text((10,410), "Coming up:")
    draw.text((10,425), hText)
    draw.text((10,440), lText)

    if testing:
        tideClock.save('tide_clock.png')
    else:
        epd.display(epd.getbuffer(tideClock))
        logging.info("Goto Sleep...")
        epd.sleep()

location = "Inlet (Coast Guard Station), Indian River, Delaware" # location input 

font24 = ImageFont.truetype(('Font.ttc'), 24)
font18 = ImageFont.truetype(('Font.ttc'), 18)
font12 = ImageFont.truetype(('Font.ttc'), 12)
points = [(187, 209), (197, 209), (192, 50)]
origin = (192, 192)
rotationMin = (360/745)


logging.basicConfig(level=logging.INFO)
if not testing:
    epd = epd7in5.EPD()
    logging.info("Init and Clear")
    epd.init()

try:
    logging.info("Tide Clock demo")
    while 1:
        update()
        time.sleep(60)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    if not testing:
        epd7in5.epdconfig.module_exit() 
    exit()
