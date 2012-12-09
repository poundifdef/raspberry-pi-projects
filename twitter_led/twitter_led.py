import signal
import sys
import time

import RPi.GPIO as gpio
import tweepy

from twitter_conf import (consumer_key, consumer_secret, access_token,
                          access_token_secret)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
# print api.me().name

keep_going = True

def signal_handler(signal, frame):
    global keep_going
    print 'quitting!'
    keep_going = False
    gpio.cleanup()

signal.signal(signal.SIGINT, signal_handler)

since_id = 1
try:
    since_id = (open('mentions.txt', 'r').read().strip())
except:
    pass

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
# api.update_status('Updating using OAuth authentication via Tweepy!')

red = 18
green = 23
blue = 24

gpio.setmode(gpio.BCM)

gpio.setup(red, gpio.OUT)
gpio.setup(green, gpio.OUT)
gpio.setup(blue, gpio.OUT)

gpio.output(red, gpio.LOW)
gpio.output(green, gpio.LOW)
gpio.output(blue, gpio.LOW)

colors = {
    'red': (1, 0, 0),
    'green': (0, 1, 0),
    'blue': (0, 0, 1),
    'yellow': (1, 1, 0),
    'cyan': (0, 1, 1),
    'magenta': (1, 0, 1),
    'white': (1, 1, 1),
}

def set_led(message):
    for k, v in colors.iteritems():
        if k in message:
            r, g, b = v
            gpio.output(red, gpio.HIGH if r else gpio.LOW)
            gpio.output(green, gpio.HIGH if g else gpio.LOW)
            gpio.output(blue, gpio.HIGH if b else gpio.LOW)
            time.sleep(3)
            gpio.output(red, gpio.LOW)
            gpio.output(green, gpio.LOW)
            gpio.output(blue, gpio.LOW)
            time.sleep(3)

while keep_going:
    print 'requesting...'
    mentions = []
    try:
        mentions = api.mentions(since_id=since_id)
    except:
        print 'no connection'

    if mentions:
        since_id = max([m.id for m in mentions])
        open('mentions.txt', 'w').write(str(since_id))

        for mention in mentions:
            print mention.text, mention.id
            set_led(mention.text)

    time.sleep(5)
