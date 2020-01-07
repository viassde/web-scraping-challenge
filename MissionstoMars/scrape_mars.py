from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


def init_browser():
    return Browser("chrome", headless=False)

def scrape_info():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='list_text')

    header_list =[]
    subheader_list =[]

    for result in results:
        # scrape the article header 
        header = result.find('div', class_='content_title').text  
        # scrape the article subheader
        subheader = result.find('div', class_='article_teaser_body').text
        
        header_list.append(header)
        subheader_list.append(subheader)
        
    news_title = header_list[0]
    news_p = subheader_list[0]


    browser.quit()
    #------------------------------------------
    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    obj1 = soup.find('div', class_='default floating_text_area ms-layer')
    obj2 = obj1.find('a')               
    href =obj2['data-fancybox-href']
    featured_image_url = url + href


    browser.quit()
    #------------------------------------------
    browser = init_browser()

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='js-tweet-text-container')

    mars_weather = results[0].find('p').text[0:-26]

    browser.quit()

    #------------------------------------------
    url = 'https://space-facts.com/mars/'
    tbl = pd.read_html(url)

    tbl_df = tbl[0]
    tbl_df.columns =['Description','Value']
    tbl_html = tbl_df.to_html(index=False)


    mars_data ={
        'news_tt': news_title,
        'news_par': news_p,
        'fimg_url': featured_image_url,
        'weather_describe': mars_weather,
        'facts_table': tbl_html,
        'valles_url': "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg",
        'cerber_url': "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg",
        'schiapa_url': "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg",
        'syrtis_url': "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"
    }



    # Return results
    return mars_data
