# Declare Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo
import requests
import time


def init_browser():
    # Use splinter to navigate the site
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    mars = {}
    
    # url for NASA's latest news
    url = "https://mars.nasa.gov/news/"

    # open the url
    browser.visit(url)
    time.sleep(2)

    # create the html
    html = browser.html

    # create beautifulsoup object
    soup = bs(html, "html.parser")

    # use soup to navigate to latest news
    news_latest = soup.find('li', class_="slide")

    # use bs object to get title and paragraph info
    news_title = news_latest.find('div', class_="content_title").a.text
    news_p = news_latest.find('div', class_="article_teaser_body").text


    # url for the mars space images
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # open the url
    browser.visit(url_img)
    time.sleep(2)

    # create html to parse
    html = browser.html

    # create beautifulsoup object
    soup = bs(html, "html.parser")

    # use soup to navigate to image
    image = soup.find('article', class_="carousel_item")["style"]
    img = image.replace("background-image: url('", "").replace("');", "")
    featured_image_url = "https://www.jpl.nasa.gov" + img

    # url of mars weather twitter account
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    time.sleep(2)

    # create html to parse
    html = browser.html

    # create beautifulsoup object
    soup = bs(html, "html.parser")

    weather = soup.find('div', attrs={"class": "css-1dbjc4n r-18u37iz", "data-testid": "tweet"})

    mars_weather = weather.find('div', attrs={"class": "css-901oao", 'dir': 'auto', 'lang': 'en'}).span.text

    # url of mars facts
    url_facts = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url_facts)

    # convert table to dataframe
    mars_facts = tables[0]

    # rename the columns
    mars_facts.columns = ["Description", "Value"]
    mars_facts.set_index("Description", inplace=True)

    # convert dataframe to an html table string
    facts_table = mars_facts.to_html()

    url_h = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_h)
    time.sleep(2)
    
    # create html to parse
    html = browser.html

    # create beautifulsoup object
    soup = bs(html, "html.parser")

    hemi = soup.find_all("div", class_="item")


    # A blank list to hold title and img
    hemisphere_image_urls = []

    # loot over h in hemi
    for h in hemi:
        title = h.find('h3').text
        img_h = h.a['href']
        url_a = "https://astrogeology.usgs.gov" + img_h

        response = requests.get(url_a)

        soup = bs(response.text, "html.parser")

        url_b = soup.find("img", class_="wide-image")["src"]
        url_c = "https://astrogeology.usgs.gov" + url_b

        hemisphere_image_urls.append({"title": title, "img_url": url_c})

    mars = {
        "news_title": news_title,
        "paragraph" : news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": facts_table,
        "hemisphere_img_urls": hemisphere_img_urls
    }

    # Close the browser after scraping
    browser.quit()
    
    return(mars)