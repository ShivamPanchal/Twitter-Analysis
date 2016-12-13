#############################################################################

# An Introduction to Text Mining using Twitter Streaming API and Python


# Author- Shivam Panchal
# shivam.panchal@mail.com

#############################################################################






'''
Text mining is the application of natural language processing techniques and analytical methods
to text data in order to derive relevant information. Text mining is getting a lot attention these
last years, due to an exponential increase in digital text data from web pages, google's projects
such as google books and google ngram, and social media services such as Twitter. Twitter data c
onstitutes a rich source that can be used for capturing information about any topic imaginable.
This data can be used in different use cases such as finding trends related to a specific keyword,
measuring brand sentiment, and gathering feedback about new products and services. 
'''


# Getting Data from Twitter Streaming API


###########################################
# Getting Data from Twitter Streaming API #
###########################################


'''
API stands for Application Programming Interface. It is a tool that makes the interaction with computer programs and web services easy.
Many web services provides APIs to developers to interact with their services and to access data in programmatic way. For this tutorial,
we will use Twitter Streaming API to download tweets related to 3 keywords: "python", "javascript", and "ruby". Step 1: Getting Twitter API keys 
In order to access Twitter Streaming API, we need to get 4 pieces of information from Twitter: API key, API secret, Access token and Access token secret.

Follow the steps below to get all 4 elements: 
 Create a twitter account if you do not already have one.
 Go to https://apps.twitter.com/ and log in with your twitter credentials.  Click "Create New App"
 Fill out the form, agree to the terms, and click "Create your Twitter application"
 In the next page, click on "API keys" tab, and copy your "API key" and "API secret".
 Scroll down and click "Create my access token", and copy your "Access token" and "Access token secret". 
'''




'''
With the help of following piece of code, you can install any python library through the console

import pip    
def install(package):
   pip.main(['install', package])
install('tweepy')
'''
###################################################################
# Step 2: Connecting to Twitter Streaming API and downloading data#
###################################################################

#Import the necessary methods from tweepy library 
from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler 
from tweepy import Stream 
 
#Variables that contains the user credentials to access Twitter API  
access_token = "771287280438968320-BtxwzQApWCF8t19Hzyy4WBCMcpwclIO" 
access_token_secret = "r6NN5lWpxFcLHzJfJME75E4ga5JEYU6kQ9fg8wQ6cHh6v" 
consumer_key = "r1ApzHiHqZMTeupo8erTrR3Et" 
consumer_secret = "3dFoEay7IrRFEvZFA6Jkuc2mGpJ33amoGTJKETfI488YGb5Iy3" 

#This is a basic listener that just prints received tweets to stdout. 
class StdOutListener(StreamListener): 
 
    def on_data(self, data): 
        try:
			print(data)
			savefile = open("twitter_data", "a")
			savefile.write(data)
			savefile.write('\n')
			savefile.close()
			return True
		except BaseException,e:
			print('Failed on Data')
			time.sleep(5)
 
		def on_error(self, status): 
			print(status) 
 
 
if __name__ == '__main__': 
 
    #This handles Twitter authetification and the connection to Twitter Streaming API 
    l = StdOutListener() 
    auth = OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    stream = Stream(auth, l) 
 
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby' 
    stream.filter(track=['python', 'javascript', 'ruby']) 

# Run the program, and it starts extracting tweets in json format, you can run it for as much as time you want it to extract tweets for you.
'''

Now, when you think you want to stop, you just write;

python twitter_mining.py < twitter_data.txt

And, its done ,now you have this info in txt format.

'''

'''
Now, we will be using 4 Python libraries json for parsing the data,
pandas for data manipulation, matplotlib for creating charts, adn re for regular expressions. The json
and re libraries are installed by default in Python. You should install pandas and matplotlib if you
don't have them in your machine.

'''

import json
import pandas as pd
import matplotlib.pyplot as plt

# Next we will read the data in into an array that we call tweets. 

tweets_data_path = ""C:\\user\Shivam Panchal\Documents\twitter_data.txt""
 
tweets_data = [] 
tweets_file = open(tweets_data_path, "r") 
for line in tweets_file: 
    try: 
        tweet = json.loads(line) 
        tweets_data.append(tweet) 
    except: 
        continue


print(len(tweets_data))


# We will start by creating an empty DataFrame called tweets using the following command. 

tweets = pd.DataFrame()


tweets['text'] = map(lambda tweet: tweet['text'], tweets_data) 
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data) 
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

# Next, we will create 2 charts: The first one describing the Top 5 languages in which the tweets were written, and the second the Top 5 countries from which the tweets were sent. 


# 1
tweets_by_lang = tweets['lang'].value_counts() 
 
fig, ax = plt.subplots() 
ax.tick_params(axis='x', labelsize=15) 
ax.tick_params(axis='y', labelsize=10) 
ax.set_xlabel('Languages', fontsize=15) 
ax.set_ylabel('Number of tweets' , fontsize=15) 
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold') 
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')



# 2
tweets_by_country = tweets['country'].value_counts() 
 
fig, ax = plt.subplots() 
ax.tick_params(axis='x', labelsize=15) 
ax.tick_params(axis='y', labelsize=10) 
ax.set_xlabel('Countries', fontsize=15) 
ax.set_ylabel('Number of tweets' , fontsize=15) 
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold') 
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue') 




# mining the TWEETS

'''

Our main goals in these text mining tasks are: compare the popularity of
Python, Ruby and Javascript programming languages and to retrieve programming
tutorial links. We will do this in 3 steps:

 We will add tags to our tweets DataFrame in order to be able to manipualte the data easily.
 Target tweets that have "pogramming" or "tutorial" keywords.
 Extract links from the relevants tweets

'''


# First, we will create a function that checks if a specific keyword is present in a text. We will do this by using regular expressions. Python provides a library for regular expression called re.
# We will start by importing this library


import re
# Next we will create a function called word_in_text(word, text). This function return True if a word is found in text, otherwise it returns False. 


def word_in_text(word, text): 
    word = word.lower() 
    text = text.lower() 
    match = re.search(word, text) 
    if match: 
        return True 
    return False 

# Next, we will add 3 columns to our tweets DataFrame. 
tweets['python'] = tweets['text'].apply(lambda tweet: word_in_text('python', tweet)) 
tweets['javascript'] = tweets['text'].apply(lambda tweet: word_in_text('javascript', tweet)) 
tweets['ruby'] = tweets['text'].apply(lambda tweet: word_in_text('ruby', tweet)) 

# We can calculate the number of tweets for each programming language as follows: 

print tweets['python'].value_counts()[True] 
print tweets['javascript'].value_counts()[True] 
print tweets['ruby'].value_counts()[True]


prg_langs = ['python', 'javascript', 'ruby'] 
tweets_by_prg_lang = [tweets['python'].value_counts()[True], tweets['javascript'].value_counts()[True], tweets['ruby'].value_counts()[True]] 
 
x_pos = list(range(len(prg_langs))) 
width = 0.8 
fig, ax = plt.subplots() 
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g') 
 
# Setting axis labels and ticks 
ax.set_ylabel('Number of tweets', fontsize=15)


ax.set_title('Ranking: python vs. javascript vs. ruby (Raw data)', fontsize=10, fontweight='bold') 
ax.set_xticks([p + 0.4 * width for p in x_pos]) 
ax.set_xticklabels(prg_langs) 
plt.grid()

'''
This shows, that the keyword ruby is the most popular, followed by python then javascript. However,
the tweets DataFrame contains information about all tweets that contains one of the 3 keywords and
doesn't restrict the information to the programming languages. For example, there are a lot tweets
that contains the keyword rubyand that are related to something else. In the next section, we will
filter the tweets and re-run the analysis to make a more accurate comparison.
'''

# Targeting relevant tweets
'''
We are intersted in targetting tweets that are related to programming languages. Such tweets often have one of the 2 keywords:
"programming" or "tutorial". We will create 2 additional columns to our tweets DataFrame where we will add this information. '''


tweets['programming'] = tweets['text'].apply(lambda tweet: word_in_text('programming', tweet)) 
tweets['tutorial'] = tweets['text'].apply(lambda tweet: word_in_text('tutorial', tweet))

'''
We will add an additional column called relevant that take value True if the tweet has either "programming" or "tutorial" keyword, otherwise it takes value False. '''

tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('programming', tweet) or word_in_text('tutorial', tweet))
'''
We can print the counts of relevant tweet by executing the commands below.
'''


print tweets['programming'].value_counts()[True] 
print tweets['tutorial'].value_counts()[True] 
print tweets['relevant'].value_counts()[True]

''' 
We can compare now the popularity of the programming languages by executing the commands below. 
'''

print tweets[tweets['relevant'] == True]['python'].value_counts()[True] 
print tweets[tweets['relevant'] == True]['javascript'].value_counts()[True] 
print tweets[tweets['relevant'] == True]['ruby'].value_counts()[True] 

# Python is the most popular with maximum count , followed by javascript, and ruby. We can make a comparaison graph by executing the commands below:



tweets_by_prg_lang = [tweets[tweets['relevant'] == True]['python'].value_counts()[True],  
                      tweets[tweets['relevant'] == True]['javascript'].value_counts()[True],  
                      tweets[tweets['relevant'] == True]['ruby'].value_counts()[True]] 
x_pos = list(range(len(prg_langs))) 
width = 0.8 
fig, ax = plt.subplots() 
plt.bar(x_pos, tweets_by_prg_lang, width,alpha=1,color='g') 
ax.set_ylabel('Number of tweets', fontsize=15) 
ax.set_title('Ranking: python vs. javascript vs. ruby (Relevant data)', fontsize=10, fontweight='bold') 
ax.set_xticks([p + 0.4 * width for p in x_pos]) 
ax.set_xticklabels(prg_langs) 
plt.grid()   





# Extracting links from the relevant tweets
'''
Now that we extracted the relevant tweets, we want to retrieve links to programming tutorials.
We will start by creating a function that uses regular expressions for retrieving link that start with "http://" or "https://" from a text.
This function will return the url if found, otherwise it returns an empty string
'''

def extract_link(text): 
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+' 
    match = re.search(regex, text) 
    if match: 
        return match.group() 
    return ''

# Next, we will add a column called link to our tweets DataFrame. This column will contain the urls information.

tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))

# Next we will create a new DataFrame called tweets_relevant_with_link. This DataFrame is a subset of tweets DataFrame and contains all relevant tweets that have a link. 

tweets_relevant = tweets[tweets['relevant'] == True] 
tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != ''] 

# We can now print out all links for python, javascript, and ruby by executing the commands below: 

print tweets_relevant_with_link[tweets_relevant_with_link['python'] == True]['link'] 
print tweets_relevant_with_link[tweets_relevant_with_link['javascript'] == True]['link'] 
print tweets_relevant_with_link[tweets_relevant_with_link['ruby'] == True]['link'] 

