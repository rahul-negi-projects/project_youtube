import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen

import concurrent.futures

import pandas as pd
from datetime import datetime
import math
import time 
import re

starttime = datetime.now()
service = Service(executable_path='chrome_driver\chromedriver.exe')
options = Options()
options.add_argument('--headless=new')    
driver = webdriver.Chrome(service=service, options=options)

# channel = 'studyiqofficial'#input('search for channel : ')
# url = "https://www.youtube.com/@" + channel + '/videos'
# videos = 100

# ---------------------------calculating maximum scrolls--------------------------- #
def max_scrolls(no_of_videos):
    if no_of_videos <= 60:
        return 1
    else:
        n = 1 + (math.ceil((no_of_videos-60)/30))
        return n

# ---------------------------extracting meta-data--------------------------- #

def videos_links(max_scrolls,url):
    driver.get(url=url)

    scroll_pause = 1
    for i in range(max_scrolls):
        try:
            driver.execute_script(f"window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(scroll_pause)
        
        except MemoryError as mem_error:
            print(f'memory error: retry {mem_error}')
        except Exception as e:
            print(f'exception: retry {e}')

    page_content = driver.page_source.encode('utf-8').strip()
    page_html = bs(page_content, 'html.parser')
    return page_html

# ---------------------------calling partucular vidoes--------------------------- #

def url_client(link):
    soup = bs(urlopen(url=link).read(),'html.parser')
    # meta_data   = soup.find_all('meta')
    likes       = (f"{soup.find('meta', itemprop='interactionCount')['content']}")
    duration    = (f"{soup.find('meta', itemprop='duration')['content']}").split('PT')[-1]
    views       = (f"{soup.find('meta', itemprop='interactionCount')['content']}")
    uploads     = (f"{soup.find('meta', itemprop='datePublished')['content']}")
    description = (f"{soup.find('meta', itemprop='description')['content']}")
    genre       = (f"{soup.find('meta', itemprop='genre')['content']}")
    # live        = (f"{soup.find('meta', itemprop='isLiveBroadcast')['content']}")
    return(likes,genre,duration,views,uploads,description)

# ---------------------------calling the function--------------------------- #

def process_video(video_url):
    likes, genre, duration, views, uploads, description = url_client(link=video_url)
    return likes, genre, duration, views, uploads, description
