import pandas as pd
import streamlit as st
import tweepy
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

# Authentication

consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# ---------------

## Defining functions for scraper

# Find recent tweets by a user (by screen name)
def user_recent(screen_name):
    tweets = api.user_timeline(screen_name, exclude_replies=True, count=200)

    text, created_at = [], []

    for tweet in tweets:
        text.append(tweet.text)
        created_at.append(tweet.created_at)

    df = pd.DataFrame(list(zip(created_at, text)),
                      columns=['created_at', 'tweet'])

    return df


# Find the recent tweets related to a key word
def word_recent(search_word, date_since):
    search_word += " -filter:retweets"

    # Find the recent tweets related to a key word
    tweets = tweepy.Cursor(api.search,
                           q=search_word,
                           lang="en",
                           since=date_since).items(20)

    text, user, location = [], [], []

    for tweet in tweets:
        text.append(tweet.text)
        user.append(tweet.user.screen_name)
        location.append(tweet.user.location)

    df = pd.DataFrame(list(zip(user, location, text)),
                      columns=['user', 'user_location', 'tweet'])

    return df


# Adding stopwords
stopwords = set(STOPWORDS)
stopwords = stopwords.union(set(['http', 'https', 'co', 'com', 't', 's', 'RT']))

twitter_mask = np.array(Image.open("twitter_bird.jpg"))

# Function to generate a word cloud
def word_cloud(lines):


    st.set_option('deprecation.showPyplotGlobalUse', False)

    text = ''

    for each in lines:
        text += ' '.join(each.split(' '))

    # Create and generate a word cloud image:
    wc = WordCloud(background_color="white", stopwords=stopwords, mask = twitter_mask).generate(text)

    # Display the generated image:
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    st.pyplot()


# -----------------------

if __name__ == '__main__':

    st.title('Twitter Scrapper Application')

    image = Image.open('twitter.jpg')

    st.image(image, caption='See what’s happening in the world right now!', width=500)

    st.subheader(
        'Real time tweets are extracted from Twitter API using the tweepy library for the tasks limited to the '
        'ones mentioned below.')

    option = st.selectbox(
        'How would you like to scrape the tweets?',
        ('Recent tweets by a user', 'Recent tweets related to a search word'))

    if (option == 'Recent tweets by a user'):

        screen_name = st.text_input('Enter the screen name (Default : @POTUS)', '@POTUS')

        st.text('Displaying the recent tweets by ' + screen_name + '.....')

        df = user_recent(screen_name)

        st.dataframe(df)

        st.text('You can also create a word cloud from the tweets text')

        if st.button('Generate Word Cloud'):
            word_cloud(df['tweet'])


    else:

        search_word = st.text_input('Enter a search word (Default : #covid)', '#covid')

        st.text('Displaying the recent tweets related to ' + search_word + '.....')

        date_since = "2021-01-01"

        df = word_recent(search_word, date_since)

        st.dataframe(df)

        st.text('You can also create a word cloud from the tweets text')

        if st.button('Generate Word Cloud'):
            word_cloud(df['tweet'])
