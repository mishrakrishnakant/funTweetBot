from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
import tweepy

from tweepy import Stream

import re,json,time, csv

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
        details = json.loads(data)
        #Get the user id so that we can send request
        userid=str(details["user"]["id"])
        screen_name=details["user"]["screen_name"]
        tweet_id=str(details["id_str"])
        #temp=api.create_favorite(tweet_id) # Favorite tweets from trending topics
        tweet_text=details["text"]
        tweetrow=[[userid, screen_name,tweet_id,tweet_text.encode('utf-8')]]
        with open("output.csv", "a") as myfile:
            writer = csv.writer(myfile)
            writer.writerows(tweetrow)
            #myfile.write(u' '.join((userid, "\t",screen_name,"\t",tweet_id,"\t",tweet_text)).encode('utf-8').strip())
        #print(details) #prints whatever we want it to print for current execution
        return True
        	
    def retweet(self, async=False):
        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening

# Before streaming find all followers

class StdOutListenerFav(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    
    def on_data(self, data):
        details = json.loads(data)
        tweet_id=details["id_str"]
        userid=details["user"]["id"]
        temp=api.create_favorite(tweet_id) # Favorite tweets from trending topics
        api.create_friendship(userid)
        return True


friend_id = []
for page in tweepy.Cursor(api.friends_ids, screen_name="funTweetBot").pages():
    friend_id.extend(page)
    print("waiting")
    time.sleep(2)

#Find all my follows now

follower_id =[]
for page in tweepy.Cursor(api.followers_ids, screen_name="funTweetBot").pages():
    follower_id.extend(page)
    print("waiting")
    time.sleep(2)


# friendships with people who do not follow

people_not_friend = list(set(friend_id) - set(follower_id))

#api.update_status("I am going on an #unfollow streak now")
#end friendship with them

for friend_not_following in people_not_friend:
    api.destroy_friendship(friend_not_following) 
    #print(friend_not_following) # print id of the person with whose the friendship was destroyed

# Find trending topics, selected area is USA with WOEID = 23424977

#api.update_status("Let us see what is the most trending topics right now")

api_results = api.trends_place(23424977,[])

trend_names=[] # contains all current trends
for location in api_results:
    for trend in location["trends"]:
        trend_names.append(trend["name"])
        #print(trend_names)
        #Streaming Class Inovccation
        stream = Stream(auth, StdOutListener())

        # create a separate stream for each invocation
        stream.filter(track=trend["name"],languages=['en'])


#write logic to fav certain tweets, we will do that for tweets about olympics only and send friend request

stream2= Stream(auth, StdOutListenerFav())
stream2.filter(track=['rioolympics'],languages=['en'])




#in future write a script that if someone was messaged and they responded,  we send them a DM or something on those lines