from selenium import webdriver
import time
import csv
import os


def get_tweets(url, statename):
    """
    Get tweets by scrolling down a Twitter search page
    :return:
    """
    # Open search page in a browser
    browser = webdriver.Safari()
    browser.get(url)
    browser.maximize_window()

    # Dismiss login element
    page_body = browser.find_element_by_class_name('container')
    page_body.click()

    # For checking if it's possible to scroll further
    page = browser.find_element_by_id('page-container')
    win_height = page.size['height']
    reached_bottom = False

    # Scroll down the page until no new tweets are loaded
    while not reached_bottom:
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)

        new_win_height = page.size['height']

        # If the page is not growing, wait a second time
        if new_win_height == win_height:
            time.sleep(10)
            if win_height == page.size['height']:
                reached_bottom = True
        else:
            win_height = new_win_height

    # Get tweets from html file
    tweets = browser.find_elements_by_class_name('tweet-text')
    tweet_texts = [[t.text] for t in tweets]

    # Save tweet texts in CSV
    filename = '{0}.csv'.format(statename.lower())
    outfile = open(filename, 'w', encoding='utf-8')
    csv.writer(outfile).writerows(tweet_texts)
    outfile.close()

    # Fin
    browser.close()


def main():
    # url template for Twitter's search age
    url_template = 'https://twitter.com/search?l=en&q=mad%20near%3A%22{0}%2C%20USA%22%20within%3A15mi&src=typd'

    if not os.path.exists('state_tweets'):
        os.mkdir('state_tweets')

    save_dir = 'state_tweets/'

    # get Tweets by locality
    get_tweets(url_template.format('Maine'), '{0}maine'.format(save_dir))
    # get_tweets(url_template.format('New Hampshire'), '{0}newhampshire'.format(save_dir))
    # get_tweets(url_template.format('Vermont'), '{0}vermont'.format(save_dir))
    # get_tweets(url_template.format('Massachusetts'), '{0}massachusetts'.format(save_dir))
    # get_tweets(url_template.format('Rhode Island'), '{0}rhodeisland'.format(save_dir))
    # get_tweets(url_template.format('Connecticut'), '{0}connecticut'.format(save_dir))


if __name__ == '__main__':
    main()
    exit(0)
