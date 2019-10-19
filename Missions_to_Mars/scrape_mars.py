# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import os
import pandas as pd


def scrape():
    executable_path = {'executable_path': 'C:chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Create a dictionary for all of the scraped data
    mars_data = {}
    # Retrieve page with the requests module

    # Create BeautifulSoup object; parse with 'html.parser'
    #Getting all article titles and article description from home page

    url2 = 'https://mars.nasa.gov/news/'
    response = requests.get(url2)
    soup = BeautifulSoup(response.text, features="lxml")

    titles = []
    title_results = soup.find_all('div', class_="content_title")
    for i in title_results:
        titles.append(i.text)

    paragraphs = []
    p_results = soup.find_all('div', class_="rollover_description_inner")
    for i in p_results:
        paragraphs.append(i.text)


    mars_data["news_titles"] = titles[0]
    mars_data["summarys"] = paragraphs[0]

    ##Mars Weather

    url3 = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)
    soup = BeautifulSoup(response.text, "html.parser")

    #create empty list for weather tweets
    weather_tweets = []
    #scrape html for tweets
    tweet_results = soup.find_all('div', class_="js-tweet-text-container")
    #find weather tweets only
    for i in tweet_results:
        if "sol" in i.text:
            weather_tweets.append(i.text)

    mars_data["Weather"] = weather_tweets[0]

    #Mars Facts

    url4 = 'https://space-facts.com/mars/'
    #use pandas to scrape url
    tables = pd.read_html(url4)
    mars_data["tables"] = tables
   
    #Scrape for featured Image
    url3 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url3)
    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `featured_image_url`
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    mars_data["featured_img"] = img_url

    #Mars Hemisphere
    #Create dictionaries with the image url string and the hemisphere title to a list.
    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)

    # Use splinter to loop through the 4 images and load them into a dictionary
    import time 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_url=[]

    # loop through the four tags and load the data to the dictionary
 
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_url.append(dictionary)
        browser.back()  
    
    mars_data['hempispher_image'] = hemisphere_image_url
    return mars_data



if __name__ == "__main__":
    print(scrape())

