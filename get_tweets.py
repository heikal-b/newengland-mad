from selenium import webdriver
import time
import csv


def main():
    """
    Get tweets by scrolling down a Twitter search page
    :return:
    """
    # Open search page in a browser
    browser = webdriver.Safari()
    url = 'https://twitter.com/search?src=typd&q=mad%20near%3A%22Massachusetts%2C%20USA%22%20within%3A15mi'
    browser.get(url)
    browser.maximize_window()

    # Dismiss login element
    page_body = browser.find_element_by_class_name('container')
    page_body.click()

    # win_size = browser.get_window_size() # needed in the future

    # Scroll down page
    for i in range(5):
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        # new_win_size = browser.get_window_size() # needed in the future

    # Get tweets
    tweets = browser.find_elements_by_class_name('tweet-text')
    tweet_texts = [[t.text] for t in tweets]

    # Save tweet texts in CSV
    outfile = open('tweets.csv', 'w')
    csv.writer(outfile).writerows(tweet_texts)
    outfile.close()

    # Fin
    browser.close()


if __name__ == '__main__':
    main()
    exit()