import pickle
import nltk
from nltk.corpus import words as eng_words
import csv


def get_next_word(tweet, target_word):
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

    tweets = pickle.load(open('adverbial_mad_tweets.pickle', 'rb'))

    print('Number of tweets:', len(tweets))

    certain_tweets = []
    uncertain_tweets = []

    eng_dict = dict.fromkeys(eng_words.words(), None)

    for t in tweets:
        next_word = get_next_word(t, 'mad')

        if not next_word:
            continue

        try:
            nw = eng_dict[next_word]
            certain_tweets.append(t)
        except KeyError:
            uncertain_tweets.append(t)

    outfile_certain = open('certain_tweets.csv', 'w', encoding='utf-8')
    csv.writer(outfile_certain).writerows([t] for t in certain_tweets)
    pickle.dump(certain_tweets, open('certain_tweets.pickle', 'wb'))

    outfile_uncertain = open('uncertain_tweets.csv', 'w', encoding='utf-8')
    csv.writer(outfile_uncertain).writerows([t] for t in uncertain_tweets)
    pickle.dump(uncertain_tweets, open('uncertain_tweets', 'wb'))


