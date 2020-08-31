from splinter import Browser
import pandas as pd
import pymongo
from flask import Flask
from bs4 import BeautifulSoup
import requests

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_p = scrape_news()

    mars_dict= {}

    mars_dict['title'] = news_title
    mars_dict['paragraph'] = news_p

    mars_dict['main_image'] = scrape_mars_image()

    mars_dict['mars_facts'] = mars_facts()

    mars_dict['mars_hemispheres'] = mars_hemisphere()

    browser.quit()
    return mars_dict 

# Mars News
def scrape_news():

    #url to be scraped
    url = 'https://mars.nasa.gov/news/'
    #retrive page w/ request module
    response = requests.get(url)
    browser.visit(url)
    #create bs object and parse w/ html parser
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())
    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text
    try:
        news_title = soup.find('div', class_= 'content_title').text
        news_p = soup.find('div', class_= 'rollover_description').text
        #print(news_title)
        #print(news_p)
    except AttributeError:
        return None, None
    #browser.quit()

    return news_title, news_p

# Mars Image
def scrape_image():
        #url to be scraped
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        #retrive page w/ request module
        response = requests.get(url)
        browser.visit(url)
        #create bs object and parse w/ html parser
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup.prettify())
    try:
        relative_image_path = soup.find_all('img')[2]["src"]
        carousel_item = url + relative_image_path
        #print(carousel_item)
    except AttributeError:
        return None, None 

# Mars Facts 
def scrape_facts():
    #url to be scraped
    url = 'https://space-facts.com/mars/'
    #retrive page w/ request module
    response = requests.get(url)
    browser.visit(url)
    tables = pd.read_html(url)
    mars_facts = tables[0]
    mars_facts.columns = ['Description','Value']
    mars_facts.to_html(header = False, index = False)
    return mars_facts

# Mars Hemispheres
def scrape_hemispheres():
    #url to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #retrive page w/ request module
    response = requests.get(url)
    browser.visit(url)
    #create bs object and parse w/ html parser
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())
    #scrape  USGS Astrogeology 
    hemisphere = soup.find_all('div', class_='item')
    USGS_url = 'https://astrogeology.usgs.gov'

    #loop through all images (reference activity 5 mongo scraping)
for hemis in hemisphere:
    #Store title
    title = hemis.find("h3").text
    # Store link of the image
    temp_img = hemis.find('a', class_= 'itemLink product-item')['href']
    
    #visit the link
    browser.visit(USGS_url + temp_img)
    
    temp_img_html = browser.html
    
    soup_img_html = BeautifulSoup(temp_img_html, 'html.parser')
    
    full_img_url = USGS_url + soup_img_html.find('img', class_='wide-image')['src']
    
    hemisphere_image_url.append({"title":title, "img_url":full_img_url})
   
hemisphere_image_url