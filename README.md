# newengland-mad
Adverbial *mad* in New England English - a study on Twitter data

Stages:

1) Data collection. For this, instances of 'mad' is collected from Twitter, using *get_tweets.py.*
The collected data files (CSV) by New England states can be found in the folder *state_tweets*. Please note that the search term in the data collection covers all instanceof 'mad'; further processing needs to be conducted to obtain only the adverbial *mad*.

2) First filtering. Tweets collected from Twitter are filtered for the adverbial usage of *mad*. This is done with filter_1/filter_mad.py. The tweets are segregated into different CSV files therein according to whether it contains adverbial *mad*. 

3) Second filtering. The first filtering obtained mostly cases of adverbial *mad*. However, there are some false positives. In general the false positives involve highly colloquial terms or abbreviations which have been confused as adjectives following *mad*.

4) The finalized data are in finalized_data.csv

5) Exploratory work