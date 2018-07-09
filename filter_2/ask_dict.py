# New England Mad - verify potential false postives of adverbial mad
# Author: Heikal Badrulhisham, <heikal93@gmail.com>
# Year: 2018
"""
Verify false positive cases of tweets with adverbial mad. For this the word next to mad is submitted to an online
dictionary (Merriam-Webster) to determine if it's an adjective
"""
import csv
import urllib.request
from urllib.error import HTTPError
import nltk
import pickle
from bs4 import BeautifulSoup


def is_adj(word):
    """
    Submits a word to Merriam-Webster's website and tells if the word is an adjective
    :param word: the word to be submitted
    :return: True if the word is an adjective, otherwise False
    """
    # Merriam-Webster URL
    mer_webs = 'https://www.merriam-webster.com/dictionary/{0}'
    # Insert search term into the URL
    url = mer_webs.format(word)

    # Get the webpage with the search term
    try:
        webpage = urllib.request.urlopen(url)
        soup = BeautifulSoup(webpage, 'html.parser')
    except HTTPError:
        return False

    # Find the POS datum
    try:
        pos_element = soup.find('span', {'class': 'fl'}).find('a')
        pos = pos_element.string
        return pos.string == 'adjective'
    except AttributeError:
        return False

    return False


if __name__ == '__main__':
    # Get the tweets which are not certain to contain adverbial mad
    csv_reader = csv.reader(open('uncertain_tweets.csv'))
    # List for accepted tweets
    accepted_tweets = []

    # For each tweet, submit the word next to mad to an online dictionary
    for tweet in csv_reader:
        # Preprocess
        tweet_tokenized = nltk.word_tokenize(tweet[0].lower())

        # Get the word next to mad
        index = tweet_tokenized.index('mad')

        # Ignore the tweet if the word is not an adjective
        if index == len(tweet_tokenized) - 1:
            continue

        # Otherwise save it
        if is_adj(tweet_tokenized[index+1]):
            accepted_tweets.append(tweet[0])

    # Save verified tweets
    pickle.dump(accepted_tweets, open('uncertain_verified.pickle', 'wb'))
    savecsv = open('uncertain_verified.csv', 'w', encoding='utf-8')
    csv.writer(savecsv).writerows([t] for t in accepted_tweets)

    exit(0)