import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle


def main():
    """
    Get tweets by scrolling down a Twitter search page
    :return:
    """
    browser = webdriver.Safari()

    url = 'https://twitter.com/search?src=typd&q=mad%20near%3A%22Massachusetts%2C%20USA%22%20within%3A15mi'
    browser.get(url)
    browser.maximize_window()

    page_body = browser.find_element_by_class_name('container')
    page_body.click()

    win_size = browser.get_window_size()

    for i in range(5):
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(5)
        new_win_size = browser.get_window_size()

    tweet_texts = browser.find_elements_by_class_name('tweet-text')
    save_file = open('tweets.pickle', 'wb')
    pickle.dumps(tweet_texts, save_file)
    save_file.close()

    for tweet in tweet_texts:
        print(tweet.text)

    browser.close()


if __name__ == '__main__':
    main()
    exit()