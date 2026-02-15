from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
import requests
import json


def handle_none_attr(data):
    try:
        val = data.get_text()
    except:
        val = "No Specified Value"
    return val

def open_page(link):
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    proxy_api_key = ""
    proxy_url =  ("scraperapi.follow_redirect=false.render=true.retry_404=true.country_code=eu.device_type=desktop:%s@proxy-server.scraperapi.com:8001" % (proxy_api_key))
    proxies = {"http": proxy_url}
    try:
        req = requests.get(link, proxies=proxies, verify=False)
    except:
        print("error")
    soup = BeautifulSoup(req.text, 'html5lib')
    return soup

def get_amazon_listings(ebay_title):
    products_list = {}
    count = 0

    payload = { 'api_key': '', 'query': ebay_title }
    r = requests.get('https://api.scraperapi.com/structured/amazon/search', params=payload)
    results = (json.loads(r.text))
    for item in results["results"]:
        #print(item)
        amz_product_title = item["name"]
        print(amz_product_title)
        amz_product_price = item["price"]
        products_list[count] = {"title": amz_product_title , "price": amz_product_price}
        count = count + 1
    
    return products_list
    
def get_scraper_stats():
    payload = {'api_key': ''}
    r = requests.get('http://api.scraperapi.com/account', params=payload)
    print(r.text)

get_scraper_stats()

def get_search_paramters():
    search_term_dict = {    "search_details":
                            {   "search_term":"hp cartridge", 
                                "product_limit":60,
                            },
                            "search_details1":                           
                            {
                                "search_term":"Epson", 
                                "product_limit":120,
                            },
                            "search_details2":                           
                            {
                                "search_term":"Razer", 
                                "product_limit":120,
                            },
                            "search_details3":                           
                            {
                                "search_term":"Logitech", 
                                "product_limit":120,
                            },
                            "search_details4":                            
                            {
                                "search_term":"Headphones", 
                                "product_limit":240,
                            },
                            "search_details5":                           
                            {
                                "search_term":"Printer", 
                                "product_limit":60,
                            },
                            "search_details6":                           
                            {
                                "search_term":"Tools", 
                                "product_limit":480,
                            },
                            "search_details7":                           
                            {
                                "search_term":"Encyclopedia", 
                                "product_limit":30,
                            },
                            "search_details8":                           
                            {
                                "search_term":"Handbook", 
                                "product_limit":60,
                            },
                            "search_details9": 
                            {
                                "search_term":"Toner", 
                                "product_limit":60,
                            },
                            "search_details10": 
                            {
                                "search_term":"Hairdryer", 
                                "product_limit":30,
                            },
                            "search_details11": 
                            {
                                "search_term":"Net gear", 
                                "product_limit":20,
                            },
                            "search_details12": 
                            {
                                "search_term":"Hair straightener", 
                                "product_limit":20,
                            }
                        }
    return search_term_dict

def build_ebay_link(search_term):
    link = ""
    search_link = "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw="
    bin_link = "&rt=nc&LH_BIN=1"
    ipg_link = "&_ipg=240"
    condition_link  = "&LH_ItemCondition=3"
    best_match_link = "&_sop=10"

    link = (search_link + search_term + bin_link + condition_link + ipg_link + best_match_link)
    link = link.replace(" ","+")

    return link


