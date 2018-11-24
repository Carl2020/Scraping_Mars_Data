# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd

# Establish browser to call up URLs for scraping
def init_browser():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# Define scrape function and initialize Dictionary to hold scrape results
def scrape():
    browser = init_browser()
    # initialize dictionary at start of scrape to prevent dups
    scrape_results = {}

# Call up Mars news url for scraping
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

# Use Beautiful Soup to parse out the url
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

# Set the parent level division for parsing
    news = soup.find('div', class_='content_title')
    news_title = news.select_one('a').text

    news_p = soup.find('div', class_='article_teaser_body').text

# Insert results into Dictionary scrape_results
    scrape_results['news_title'] = news_title
    scrape_results['news_text'] = news_p

# Call up the Jet Propulsion Labs website for latest featured Mars image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

# Scrape for latest image and store in dictionary
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('section', class_='centered_text clearfix main_feature primary_media_feature single')
    link = image.find('a')['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov{link}'
    scrape_results['featured_image_url'] = featured_image_url

# Twitter URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

# Retrieve the parent divs for all articles
    results = soup.find_all('div', class_='js-tweet-text-container')

    weather_report = []
    for result in results:
        report = result.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
        weather_report.append(report)

    scrape_results['mars_weather'] = weather_report[0]

# Use pandas to read in table data from space_facts site re: Mars facts
    url = 'http://space-facts.com/mars/'

    tables = pd.read_html(url)

# convert tables into a Pandas Dataframe
    df = tables[0]
    df.columns = ['Characteristic', 'Measure']
    df.head(10)

# Convert Pandas dataframe into an html formatted table
    marsfacts_html_table = df.to_html()

# Add the mars facts html table to our dictionary
    scrape_results['mars_facts'] = marsfacts_html_table

# URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'

# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

# Retrieve the parent div for all hemispheres
    result = soup.find('div', class_='downloads')

    cerberus_url = result.a['href']

    title = soup.find('div', class_='content')

    cerberus_title = title.find('h2', class_='title').text

# save as a python dictionary object
    scrape_results['cerberus_title'] = cerberus_title
    scrape_results['cerberus_url'] = cerberus_url

# URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'

# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

# Retrieve the parent div for all hemispheres
    result = soup.find('div', class_='downloads')

    schiaparelli_url = result.a['href']

    title = soup.find('div', class_='content')

    schiaparelli_title = title.find('h2', class_='title').text

    scrape_results['schiaparelli_title'] = schiaparelli_title
    scrape_results['schiaparelli_url'] = schiaparelli_url

# URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'

# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

# Retrieve the parent div for all hemispheres
    result = soup.find('div', class_='downloads')

    syrtis_major_url = result.a['href']

    title = soup.find('div', class_='content')

    syrtis_major_title = title.find('h2', class_='title').text

    scrape_results['syrtis_major_title'] = syrtis_major_title
    scrape_results['syrtis_major_url'] = syrtis_major_url

# URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

# Retrieve page with the requests module
    response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

# Retrieve the parent div for all hemispheres
    result = soup.find('div', class_='downloads')

    valles_marineris_url = result.a['href']

    title = soup.find('div', class_='content')

    valles_marineris_title = title.find('h2', class_='title').text

    scrape_results['valles_marineris_title'] = valles_marineris_title
    scrape_results['valles_marineris_url'] = valles_marineris_url

    browser.quit()

# Return results
    return scrape_results

