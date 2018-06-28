# New England Mad: a function for obtaining tweets
# Author: Heikal Badrulhisham <heikal93@gmail.com>
# Year: 2018
"""
Define the get_tweets() function for loading and saving tweets through Twitter's search page in a browser. The method
opens a twitter search page with a search query and scrolls down the page repeatedly to load more tweets until there are
no more tweets to load. This is to circumvent the limitations (in terms of time span and number of requests) of the free
Twitter API. The main function here collects tweets
"""
from selenium import webdriver
from selenium.common.exceptions import *
import time
import csv
import os


def scroll_down(browser, interval=2, second_chance_interval=5):
    """
    Helper function for scrolling down a page (for get_tweets())
    :param browser: Webdriver browser instance to scroll down in
    :param interval: number of seconds to wait while loading the page
    :param second_chance_interval: number of seconds to wait for the second time
    :return:
    """
    # For checking if it's possible to scroll further
    page = browser.find_element_by_id('page-container')
    win_height = page.size['height']
    reached_bottom = False

    # Scroll down the page
    while not reached_bottom:
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(interval)

        # If the page is not growing, wait a second time
        new_win_height = page.size['height']

        if new_win_height == win_height:
            time.sleep(second_chance_interval)
            if win_height == page.size['height']:
                reached_bottom = True
        else:
            win_height = new_win_height


def get_tweets(url, save_dir, file_stem='tweets', interval=2, second_chance_interval=10):
    """
    Get tweets by scrolling down a Twitter search page and save tweets in a CSV file
    :param url: the search URl
    :param save_dir: the directory for the saved data file
    :param file_stem: the stem of the file name for saving tweets
    :param interval: number of seconds to wait while loading the page
    :param second_chance_interval: number of seconds to wait for the second time
    :return:
    """
    # Open search page in a browser
    browser = webdriver.Safari()
    browser.get(url)
    browser.maximize_window()

    # Dismiss login element if it exists, otherwise move on
    try:
        page_body = browser.find_element_by_class_name('container')
        page_body.click()
    except NoSuchElementException:
        pass

    # Scroll down the page and wait for new tweets to load
    scroll_down(browser, interval, second_chance_interval)

    # Get tweets from html file
    tweets = browser.find_elements_by_class_name('tweet-text')
    tweet_texts = [[t.text] for t in tweets]

    # Save tweet texts in CSV
    filename = '{0}/{1}.csv'.format(save_dir, file_stem)
    outfile = open(filename, 'w', encoding='utf-8')
    csv.writer(outfile).writerows(tweet_texts)
    outfile.close()

    # Fin
    browser.close()
    browser.quit()


if __name__ == '__main__':
    # url template for Twitter's search age
    url_template = 'https://twitter.com/search?l=en&q=mad%20near%3A%22{0}%2C%20USA%22%20within%3A15mi&src=typd'

    save_folder = 'state_tweets'

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    # get Tweets by state
    get_tweets(url_template.format('Maine'), save_folder, 'maine')
    # get_tweets(url_template.format('New Hampshire'), save_folder, 'newhampshire')
    # get_tweets(url_template.format('Vermont'), save_folder, 'vermont')
    # get_tweets(url_template.format('Massachusetts'), save_folder, 'massachusetts')
    # get_tweets(url_template.format('Rhode Island'), save_folder, 'rhodeisland')
    # get_tweets(url_template.format('Connecticut'), save_folder, 'test')

    exit(0)
