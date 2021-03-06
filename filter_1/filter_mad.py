# New England Mad - filter adverbial mad from course search results
# Author: Heikal Badrulhisham, <heikal93@gmail.com>
# Year: 2018
"""
Take the tweets obtained from searching by major New England cities and filter out tweets that contain the usage of
'mad' as an adverb. This step is necessary because the initial data scraping done by get_tweets_cities.py involves all
uses of 'mad'. The classifying mechanism is the is_adverbial_mad() function, which applies various syntactic tests
on the word after 'mad' to determine that it is an adjective.
"""

import os
import csv
import nltk
import logging
import pickle
import re
from nltk.corpus import words as eng_words
from filter_2.ask_dict import is_adj

eng_dict = dict.fromkeys(eng_words.words(), None)


def unigram_test(next_word):
    next_word_tag = nltk.pos_tag([next_word])[0][1]
    return next_word_tag == 'JJ'


def next_word_test(tagged_tweet, index):
    return tagged_tweet[index + 1][1] == 'JJ'


def removal_test(tweet_tokenized, index):
    mod_sent = [w for w in tweet_tokenized if w.lower() != 'mad']
    mod_sent = nltk.pos_tag(mod_sent)
    return len(mod_sent) > index and mod_sent[index][1] == 'JJ'


def new_sent_test(next_word):
    test_phrase = ['the', 'really', next_word, 'dog']
    test_phrase_2 = ['the', next_word, 'dog']

    test_phrase_tagged = nltk.pos_tag(test_phrase)
    test_phrase_2_tagged = nltk.pos_tag(test_phrase_2)

    return test_phrase_tagged[2][1] == 'JJ' and test_phrase_2_tagged[1][1] != 'NN'


def is_eng_word(word):
    # Dictionary for looking up words next to mad
    try:
        w = eng_dict[word]
    except KeyError:
        return False
    return True


def is_adverbial_mad(tweet):
    """
    Determine if a tweet contains an adverbial 'mad'
    :param tweet: tweet text as a string
    :return: True if there is an adverbial 'mad'
    """
    # Preprocess the tweet
    tweet_tokenized = nltk.word_tokenize(tweet)
    tagged_tweet = nltk.pos_tag(tweet_tokenized)

    # Adjacent tags that should not follow 'mad'
    exc_tags = ['CC', 'CS', 'IN', 'PRP']
    forbidden_words = ['i', "i'll"]
    arbitrary_list = ['funny']

    # If the tweet has no 'mad' at all
    try:
        index = tweet_tokenized.index('mad')
    except ValueError:
        return False

    # If mad is at the end of the tweet, or before punctuation
    if index == len(tweet_tokenized) - 1 or not tweet_tokenized[index+1].isalpha():
        return False

    # The word next to 'mad'
    next_word = tweet_tokenized[index + 1]

    if not is_eng_word(next_word) or tagged_tweet[index+1][1] in exc_tags or next_word.lower() in forbidden_words:
        return False

    return (unigram_test(next_word) or next_word_test(tagged_tweet, index) or removal_test(tweet_tokenized, index)
            or new_sent_test(next_word) or next_word.lower() in arbitrary_list or is_adj(next_word))


if __name__ == '__main__':
    # Data files directory
    try:
        city_files = os.listdir('../cities_tweets')
    except FileNotFoundError:
        logging.error('Directory not found.')
        exit(1)

    # For saving Tweets that do and do not pass the filter
    adverbial_mad_tweets = []
    excluded_tweets = []

    # Read each city CSV file, and each tweet therein
    for file in city_files:
        city_csv = csv.reader(open('../cities_tweets/{0}'.format(file)))
        print(file)

        for row in city_csv:
            if row[0] in excluded_tweets or row[0] in adverbial_mad_tweets:
                continue

            if is_adverbial_mad(row[0]):
                adverbial_mad_tweets.append(row[0])
            else:
                excluded_tweets.append(row[0])

    adverbial_mad_tweets = list(set(adverbial_mad_tweets))
    excluded_tweets = list(set(excluded_tweets))

    # Save the lists
    pickle.dump(adverbial_mad_tweets, open('adverbial_mad_tweets.pickle', 'wb'))
    pickle.dump(excluded_tweets, open('excluded_tweets.pickle', 'wb'))

    # Export data into CSV files
    outfile_mad = open('adverbial_mad_tweets.csv', 'w', encoding='utf-8')
    csv.writer(outfile_mad).writerows([[t] for t in adverbial_mad_tweets])
    outfile_mad.close()

    outfile_exc = open('excluded_tweets.csv', 'w', encoding='utf-8')
    csv.writer(outfile_exc).writerows([[t] for t in excluded_tweets])
    outfile_exc.close()

    exit(0)

