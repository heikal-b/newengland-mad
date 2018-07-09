# New England Mad - separating false positives of adverbial mad
# Author: Heikal Badrulhisham, <heikal93@gmail.com>
# Year: 2018
"""
Filter out false postive cases of adverbial mad after the first round of filtering. Impressionistically, the false
positive cases involve words that are not in the standard register, but were considered as adjectives by the tagger.
The word next to mad is looked up in a dictionary,and the tweets are separated according to whether the word next to mad
is in the dictionary. The tweets for which this is not true will need to be processed further
"""
import pickle
import nltk
from nltk.corpus import words as eng_words
import csv


def get_next_word(tweet, target_word):
    """
    Return the word next to the target word in a sentence
    :param tweet: sentence string
    :param target_word: target word next to which is to be returned
    :return: the word next to the target word
    """
    # Preprocess
    tweet_tokenized = nltk.word_tokenize(tweet.lower())

    # Get index of target word
    try:
        index = tweet_tokenized.index(target_word.lower())
    except ValueError:
        return ''

    # If the target is at the end
    if index == len(tweet_tokenized) - 1:
        return ''

    # Return next word
    return tweet_tokenized[index+1]


if __name__ == '__main__':
    # Load lust of tweets
    tweets = pickle.load(open('adverbial_mad_tweets.pickle', 'rb'))

    print('Number of tweets:', len(tweets))

    # List for separating tweets
    certain_tweets = []
    uncertain_tweets = []

    # Dictionary for looking up words next the mad
    eng_dict = dict.fromkeys(eng_words.words(), None)

    # Separate the tweets
    for t in tweets:
        # Get the word next to mad
        next_word = get_next_word(t, 'mad')

        if not next_word:
            continue

        # Look up the word and separate the tweet accordingly
        try:
            nw = eng_dict[next_word]
            certain_tweets.append(t)
        except KeyError:
            uncertain_tweets.append(t)

    # Save the separated tweets
    outfile_certain = open('certain_tweets.csv', 'w', encoding='utf-8')
    csv.writer(outfile_certain).writerows([t] for t in certain_tweets)
    pickle.dump(certain_tweets, open('certain_tweets.pickle', 'wb'))

    outfile_uncertain = open('uncertain_tweets.csv', 'w', encoding='utf-8')
    csv.writer(outfile_uncertain).writerows([t] for t in uncertain_tweets)
    pickle.dump(uncertain_tweets, open('uncertain_tweets', 'wb'))


