import numpy as np
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from html.parser import HTMLParser
import re 


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # scrape nasa url
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get article title
    article = soup.find_all('div', class_='content_title')
    # Get article body
    body = soup.find_all('div', class_='article_teaser_body')

    # Close the browser after scraping
    browser.quit()
    browser = init_browser()

    # Get nasa images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # scrape nasa images
    image = soup.find('article', class_='carousel_item').get('style')

    # Close the browser after scraping
    browser.quit()
    browser = init_browser()

    # scrape nasa url
    # url = "https://twitter.com/marswxreport?lang=en"
    # browser.visit(url)

    # time.sleep(3)

    # Scrape page into Soup
    # html = browser.html
    # soup = bs(html, "html.parser")

    # get article body
    # tweet = soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    
    # Close the browser after scraping
    # browser.quit()
    # browser = init_browser()

    # scrape nasa url
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # get article body
    facts = soup.find_all('tr')
    
    # Close the browser after scraping
    browser.quit()
    browser = init_browser()

    # scrape nasa url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # get article body
    pics = soup.find_all('img', class_="thumb")
    
    # Close the browser after scraping
    browser.quit()

    # function to remove html tags https://medium.com/@jorlugaqui/how-to-strip-html-tags-from-a-string-in-python-7cb81a2bbf44
    def remove_html_tags(text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    # call function and convert object to string using __repr__
    check = remove_html_tags(article.__repr__())

    # format data and split on any ,
    save = check.split(",")
    title_clean = save

    # # create and clean new dataframe
    title_clean = pd.DataFrame(title_clean)
    title_clean.columns = ['title']
    title_df = title_clean.drop([0, 13, 15, 32, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58])
    title_df.reset_index(drop=True, inplace=True)

    # call function and convert object to string using __repr__
    check_bodies = remove_html_tags(body.__repr__())

    # format data and split on any ,
    save_body = check_bodies.replace("[", '').split("., ")

    # create and clean new dataframe
    body_df = pd.DataFrame(save_body)
    body_df.columns = ['Body']
    body_df.reset_index(drop=True, inplace=True)
    
    # put body and title into 1 df
    new_df = pd.concat([title_df, body_df], axis=1)
    
    #remove characters from image scrape
    image = image.replace("background-image: url(", "")
    image = image.replace(");", "")
    image = image.replace("""'""", "")

    # call function and convert object to string using __repr__
    # tweet = remove_html_tags(tweet.__repr__())
    # tweet = tweet.split("·,")
    
    #create df and reformat
    # tweet = pd.DataFrame(tweet)
    # tweet.columns = ['tweet']
    # tweet.drop(tweet.index[[0,1,2,4,5,6,7,8]], inplace=True)
    # tweet.reset_index(drop=True, inplace=True)
    
    #save what we are targeting
    news_title = title_df.iloc[0]['title']
    news_p = body_df.iloc[0]['Body']
    featured_image_url = f"https://www.jpl.nasa.gov{image}"
    # mars_weather = tweet

    # call function and convert object to string using __repr__
    facts = remove_html_tags(facts.__repr__())
    
    # edit facts df
    facts = facts.replace("[", "").split(", ")
    facts_df = pd.DataFrame(facts)
    facts_df.columns = ['facts']
    facts_df = facts_df['facts'].str.split(":", expand = True)
    facts_df.columns = ['Info', 'Data']
    
    #last of the scrapes
    news_title = title_df.iloc[0]['title']
    news_p = body_df.iloc[0]['Body']
    featured_image_url = f"https://www.jpl.nasa.gov{image}"
    # mars_weather = tweet
    facts_dict = facts_df.to_html()
    mars_list = {
        "title" : "Cerberus Hemisphere", "img_url" : "/cache/images/dfaf3849e74bf973b59eb50dab52b583_cerberus_enhanced.tif_thumb.png",
        "title" : "Schiaparelli Hemisphere", "img_url" : "cache/images/7677c0a006b83871b5a2f66985ab5857_schiaparelli_enhanced.tif_thumb.png",
        "title" : "Syrtis Major", "img_url" : "/cache/images/aae41197e40d6d4f3ea557f8cfe51d15_syrtis_major_enhanced.tif_thumb.png",
        "title" : "Valles Marineris", "img_url" : "/cache/images/04085d99ec3713883a9a57f42be9c725_valles_marineris_enhanced.tif_thumb.png"
    }
    #create list to store all scrapes
    mars_data = {
        "news_title" : news_title,
        "news_para" : news_p,
        "featured_image_url" : featured_image_url,
        # "mars_weather" : mars_weather,
        "facts_table" : facts_dict,
        "mars_list" : mars_list,
    }
    return mars_data
