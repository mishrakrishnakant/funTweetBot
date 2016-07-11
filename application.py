from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
import tweepy

from tweepy import Stream

import re,json

from config import CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKENS_SECRET

#All import statements

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKENS_SECRET)

api = tweepy.API(auth)

#initializing all parameters for auth

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    
    def on_data(self, data):

    	#get the tweet text
    	status_start=data.index("text\":")+len("text\":")
    	status_end=data.index(",\"source",status_start)
        status = data[status_start:status_end]

        #filter the tweet by checking the first character for retweets

        if status[1] <> "R":

        	#Get the user id so that we can send request

        	details = json.loads(data)

        	userid=details["user"]["id"]

        	screen_name=details["user"]["screen_name"]
        	temp=api.create_friendship(userid)
        	print(temp) #prints if sent friend request or not, can additionally follow if specified with the parameters
        	return True
        	
    def retweet(self, async=False):
        return True

    def on_error(self, status):
        print(status)

#Streaming Class

stream = Stream(auth, StdOutListener())
stream.filter(track=['#IamABot','#Bot','#Robot','TalkToMe'],languages=['en'])

#This bot will reply to all bot in a streaming logic i.e., a worker application that does not need to be restarted constantly


# write a method to get a status for a certain keyword and extract status id


#retweet to that status

#send a friend request to them


#in future write a script that if someone was messaged and they responded,  we send them a DM or something on those lines