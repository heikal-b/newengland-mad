# New England Mad: get tweets by New England cities
# Author: Heikal Badrulhisham <heikal93@gmail.com>
# Year: 2018
"""
Load tweets from New England cities through a browser and save them in a CSV file
"""

import csv
import get_tweets
import os


if __name__ == '__main__':
    # Get a list of cities
    cities_csv = csv.reader(open('neweng_cities.csv'))
    cities = [(r[0], r[1]) for r in cities_csv]

    # Folder for saving data files
    save_dir = 'cities_tweets'

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # URL template for Twitter search page
    url_template = 'https://twitter.com/search?l=en&q=mad%20near%3A%22{0}%22%20within%3A15mi&src=typd'

    # Get tweets by city
    for city in cities:
        # Stem of the data file name
        file_name_stem = '{0}_{1}'.format(city[0], city[1])

        # Skip if tweets have been collected for the city
        if os.path.exists('{0}/{1}.csv'.format(save_dir, file_name_stem)):
            continue

        # Location term for searching (City + State abbreviation)
        location = '{0}, {1}'.format(city[0], city[1])
        curr_url = url_template.format(location)

        get_tweets.get_tweets(curr_url, save_dir, file_name_stem, 2, 2)

    exit(0)
