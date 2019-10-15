# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import os
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'C:chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    url1 = 'https://mars.nasa.gov/news/8512/nasa-mars-mission-connects-with-bosnian-and-herzegovinian-town/'

    # Retrieve page with the requests module
    response = requests.get(url1)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text)

    # scrape results for iterable list
    titles = []
    title_results = soup.find_all('h1', class_="article_title")
    for i in title_results:
        title = i.text

    paragraphs = []
    p_results = soup.find_all('p')
    for i in p_results:
        paragraph = i.text

    mars_data["news_title"] = title
    mars_data["summary"] = paragraphs
    #Getting all article titles and article description from home page

    url2 = 'https://mars.nasa.gov/news/'
    response = requests.get(url2)
    soup = BeautifulSoup(response.text)

    titles = []
    title_results = soup.find_all('div', class_="content_title")
    for i in title_results:
        titles.append(i.text)

    paragraphs = []
    p_results = soup.find_all('div', class_="rollover_description_inner")
    for i in p_results:
        paragraphs.append(i.text)


    mars_data["news_titles"] = titles
    mars_data["summarys"] = paragraphs
    ##Mars Weather

    url3 = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)
    soup = BeautifulSoup(response.text)

    #create empty list for weather tweets
    weather_tweets = []
    #scrape html for tweets
    tweet_results = soup.find_all('div', class_="js-tweet-text-container")
    #find weather tweets only
    for i in tweet_results:
        if "sol" in i.text:
            weather_tweets.append(i.text)
    #print all tweets
    #print(i.text)
    mars_data["tweets"] = weather_tweets


    #Mars Facts

    url4 = 'https://space-facts.com/mars/'
    #use pandas to scrape url
    tables = pd.read_html(url4)
    mars_data["tables"] = tables

    #Create dictionaries with the image url string and the hemisphere title to a list.
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]
    mars_data['hempispher_image'] = hemisphere_image_urls
    return mars_data

