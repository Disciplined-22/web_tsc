from flask import Flask
import pickle
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
def fetch_data():
    random_number = random.randint(0,1)

    # Function to load proxies from cache
    def load_proxies_from_cache(cache_file='proxies.pkl'):
        try:
            with open(cache_file, 'rb') as f:
                proxies = pickle.load(f)
            return proxies
        except FileNotFoundError:
            return None

    connection_string = "mongodb+srv://@.t9kkmra.mongodb.net/?retryWrites=true&w=majority"

    def save_trends_to_mongo(trends, ip_address, db_name='web_s', collection_name='web_s'):
        client = MongoClient(connection_string)  # Use the provided connection string
        db = client[db_name]
        collection = db[collection_name]
        trend_data = {
            "ip_address": ip_address,
            "trends": trends
        }
        # Insert the trend data into the collection
        collection.insert_one(trend_data)
        print("Trends saved to MongoDB", trend_data)

        # Load proxies from cache
    proxies = load_proxies_from_cache()

    if not proxies:
        print("No cached proxies found. Fetching new proxies...")
        # Fetch proxies if cache is empty or missing
        # You can call your function to fetch proxies here
        # proxies = fetch_proxies(num_proxies=10, cache_file='proxies.pkl')
    
    # Continue with the rest of your script using the proxies

    # Select one proxy from the array
    print("proxies",proxies)
    selected_proxy = proxies[1]

    # Configure the WebDriver with the selected proxy
    def configure_webdriver_with_proxy(proxy):
        chrome_options = Options()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        
        # Initialize the Chrome browser with undetected_chromedriver
        driver = uc.Chrome(options=chrome_options)
        
        return driver

    browser = configure_webdriver_with_proxy(selected_proxy)
    browser.get('https://x.com/')

    # Load cookies from pickle file
    cookies = pickle.load(open("cookies.pkl", "rb"))

    # Add cookies to the browser
    for cookie in cookies:
        cookie['domain'] = ".x.com"
        try:
            browser.add_cookie(cookie)
        except Exception as e:
            print(e)

    # Refresh the page after adding cookies
    browser.get('https://x.com/')

    time.sleep(2)

    html_data = BeautifulSoup(browser.page_source, 'html.parser')




    # Find the unique <div> tag with aria-label="Timeline: Trending now"
    trending_div = html_data.find('div', attrs={'aria-label': 'Timeline: Trending now'})



    

    
    text_set = set()
    
    if trending_div:
        if trending_div.find("div", class_="css-175oi2r r-13awgt0 r-1cwvpvk"):
        
            first_tg = trending_div.find("div",class_="css-175oi2r r-13awgt0 r-1cwvpvk")
            if first_tg.find("div",class_="css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1xuzw63", dir='ltr'):
                f_sec = first_tg.find("div",class_="css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1xuzw63", dir='ltr')
                if f_sec.find("span", class_="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3"):
                    sec_t = f_sec.find("span", class_="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3")
                else:
                    print("inner 3rd main block not present")
            else:
                print("inner main block not present")
        else:
            print("First_tg is not present, new div block not present")
        
        
        
      
        
        

        

        ltr_divs = trending_div.find_all('div', class_="css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1bymd8e", dir='ltr')
        

        if sec_t:
            for sec in sec_t:
                text_set.add(sec.text.strip())
                print("text_set_1",text_set)


        # span, css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3

        # second after
        for div in ltr_divs:
            
            span_tags_out = div.find_all('span', class_="r-18u37iz")
            span_tag_out_2 = div.find_all('span', class_="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3")
            for span_tag in span_tags_out:
                span_tags_in = span_tag.find_all('span', class_='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3', dir='ltr')
                for tag_1 in span_tags_in:
                    text_set.add(tag_1.text.strip())
                    print("text_set___2",text_set)

            for spano in span_tag_out_2:
                text_set.add(spano.text.strip())



        #last one
        span_tag_ex = trending_div.find_all('span', class_='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3', dir='ltr')
        for extag in span_tag_ex:
            
            text_set.add(extag.text.strip())
            print("text_set___3",text_set)


        

        text_array = list(text_set)
        # Print the unique hashtags array
        print(text_array)

        ip_address = selected_proxy  # Replace with the actual IP address if needed
        save_trends_to_mongo(text_array, ip_address)
        print(text_array, ip_address)
        return text_array, ip_address

    else:
        print("Trending div not found")

    # Pause execution for a while
    time.sleep(300)

    # Close the browser
    browser.quit()


if __name__ == "__main__":
    app.run(debug=True)
