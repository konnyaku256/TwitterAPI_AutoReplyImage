import tweepy
import urllib.request
import datetime

#Authorization
f = open('config.txt')
data = f.read()
f.close()
lines = data.split('\n')

def get_oauth():
	consumer_key = lines[0]
	consumer_secret = lines[1]
	access_key = lines[2]
	access_secret = lines[3]
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	return auth

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.in_reply_to_screen_name=='アイコンを変更したいtwitterのアカウントID(@以下)':
            print (status.author.screen_name)
            if 'media' in status.entities :
                medias = status.entities['media']
                m =  medias[0]
                media_url = m['media_url']
                try:
                    urllib.request.urlretrieve(media_url, 'icon.jpg')
                except IOError:
                    print ("保存に失敗しました")
                now = datetime.datetime.now()
                time = now.strftime("%H:%M:%S")
                message = '@'+status.author.screen_name+' アイコンを変更しました('+time+')'
                try:
                    api.update_profile_image('icon.jpg')
                    api.update_status(status=message, in_reply_to_status_id=status.id)
                except tweepy.error.TweepError as e:
                    print ("error response code: " + str(e.response.status))
                    print ("error message: " + str(e.response.reason))

auth = get_oauth()
api = tweepy.API(auth)
stream = tweepy.Stream(auth, StreamListener(), secure=True)
print ("Start Streaming!")
stream.userstream()