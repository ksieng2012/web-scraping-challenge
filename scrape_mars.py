# import all dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
from urllib.parse import urlsplit

# # scrape()
def scrape():
    scrape_data = {}
    marsNews = mars_news()
    scrape_data['news_title'] = marsNews['news_title']
    scrape_data['news_paragraph'] = marsNews['new_p']
    scrape_data['mars_img'] = mars_img()
    scrape_data['mars_fac'] = mars_fac()
    scrape_data['mars_hemi'] = mars_hemi()

    return scrape_data


# function to start a webpage using chromedriver
def start_web():
    executable_path = {'executable_path':"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# function for scraping mars news
def mars_news ():

    # declare output dict
    output_dict = {}

    # start brouser
    browser = start_web()

    # loading the webpage
    url = "https://mars.nasa.gov/news"
    browser.visit(url)

    # writing page to html using BeautifulSoup
    html = browser.html
    soup = bs(html, "html.parser")
    
    time.sleep(0.5)

    # extracting news title and news paragraph
    title = [title for title in [tt.a.text for tt in soup.find_all("div", class_="content_title") if tt.a] if title != ""]
    time.sleep(0.5)
    # news_p = soup.find_all("div", class_="article_teaser_body")
    para = [para.text for para in soup.find_all("div", class_="article_teaser_body")]
    time.sleep(0.5)
    # scrap date
    date = [date.text for date in soup.find_all("div", class_="list_date")]

    # output dicts
    output_dict = {'news_title': title [0], 'new_p' : para [0], 'news_d': date [0]}

    # quit broswer
    browser.quit()

    # return output
    return output_dict

# JPL Mars Space Images - Featured Image
def mars_img():
    # start brouser
    browser = start_web()

    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)
    
    time.sleep(0.5)
    
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_img))

    # Create an Xpath to graph the image
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    
    time.sleep(0.5)

    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = base_url + img_url

    # quit broswer
    browser.quit()

    return featured_image_url

# # Mars Facts
def mars_fac ():

    url_fac = "https://space-facts.com/mars/"

    # Use panda to read HTML page
    tables = pd.read_html(url_fac)
    # create proper mars dataFrames
    df_mars = tables[0].copy()
    df_mars.columns=["description", "value"]

    # convert dataFrames to HTML tables
    mars_html_table = df_mars.to_html(index = False)

    return mars_html_table


# Mars Hemispheres
def mars_hemi ():
    # start brouser
    browser = start_web()

    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_base_hemi = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemispheres))

    browser.visit(url_hemispheres)

    time.sleep(0.5)
    hemispheres_html = browser.html
    soup = bs(hemispheres_html, 'html.parser')

    # getting all contents in class_='item'
    items = soup.find_all('div', class_='item')

    # empty array
    hemisphere_image_urls = []

    for item in items:
        # getting title from h3 tag
        title = item.find('h3').text
        #getting image url from <a> tag with class "itemLink product-item"
        img_url = item.find('a', class_='itemLink product-item')['href']
        
        # visit webpage
        browser.visit(url_base_hemi+img_url)
        
        # writing broser to html
        img_html = browser.html
        soup = bs(img_html, 'html.parser')
        
        # finding jpeg link
        jpeg_url = url_base_hemi + soup.find('img', class_='wide-image')['src']
        
        # append the url as list of dict
        hemisphere_image_urls.append({'title' : title,  'jpeg_url' : jpeg_url})
        
        # set time sleep
        time.sleep(0.5)

    # quit broswer
    browser.quit()
    
    return hemisphere_image_urls