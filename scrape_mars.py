from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium import webdriver
# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()
    
    mars_data = {}
    #----------------------------------- 
    
    # Get Mars News first
    urlnews = "https://mars.nasa.gov/news/"
    browser.visit(urlnews)

    # Scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")

    article = soup.find("div", class_="list_text")
    news_p = soup.find("div", class_="article_teaser_body").text
    news_title = soup.find("div", class_="content_title").text
    news_date = soup.find("div", class_="list_date").text
    # Put Mars data into dictionary
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["information"] = news_p
    
    #-----------------------------------     
    # Get featured image
    urlfeatured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(urlfeatured)

    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find('img', class_='thumb')["src"] 
    image_url = 'https://jpl.nasa.gov'+ image 
    # Add featured image link to dictionary
    mars_data['featured_image'] =  image_url
   
    #-----------------------------------    
    # Get recent Mars weather
    urlweather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(urlweather)

    html = browser.html
    soup = bs(html, "html.parser")

    weather_list = []

    for weather in soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_list.append(weather.text)

        mars_weather = weather_list[0]
    # Add weather to dictionary
    mars_data["mars_weather"] = mars_weather    
    #-----------------------------------
    #  Get Mars facts
    urlfacts = "https://space-facts.com/mars/"
    browser.visit(urlfacts)

    html = browser.html
    soup = bs(html, "html.parser")


    tables = pd.read_html(urlfacts)
    mars_facts = pd.DataFrame(tables[0])
    mars_facts.columns = ['Details', 'Measurements']
    mars_facts.set_index('Details', inplace=False)   
    df_mars = mars_facts.to_html('mars_table_pd.html')
    df_mars = df_mars.replace('\n', ' ')
    # Add dataframe to dictionary
    mars_data["mars_info"] = df_mars
    #-----------------------------------
    #  Get Mars hemispheres
    urlhemis = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(urlhemis)

    html = browser.html
    soup = bs(html, "html.parser")

    hemi_pics = []
    image_one = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    image_two = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    image_three = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    image_four = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    hemi_pics = {"Cerberus": image_one, "Schiaparelli":image_two, "Syrtis Major":image_three, "Valles Marineris":image_four}
    # Add pics to dictionary
    mars_data['hemi_pics']= hemi_pics


    return mars_data