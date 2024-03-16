# Scraping Imports
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import SellScraperLib
import Levenshtein
import concurrent.futures
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def handle_none_attr(data):
    try:
        val = data.get_text()
    except:
        val = "No Specified Value"
    return val

def open_page(link):
    req = Request(link, headers={'User-Agent' : 'Mozilla/5.0'})
    webpage  = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html5lib')
    return soup

def get_amz_product_data(product_link):
    product_data = open_page(product_link)
    product_details = product_data.find("div", attrs= {"id":"ppd"})
    product_additional_information = product_data.find("table", attrs={"id":"productDetails_detailBullets_sections1", "class":"a-keyvalue prodDetTable"})
    try:
        buy_box = handle_none_attr(product_data.find("div", attrs={"class":"olp-text-box"}).find("span")) + " " 
        + handle_none_attr(product_data.find("div", attrs={"class":"olp-text-box"}).find("span", attrs={"class":"a-offscreen"}))
    except:
        buy_box = "no buy box"

    details = {
        "amz_title": SellScraperLib.handle_none_attr(product_data.find("span", attrs={"id":"productTitle", "class":"a-size-large product-title-word-break"})).strip(),
        "amz_price": SellScraperLib.handle_none_attr(product_data.find("div", attrs={"class":"a-section a-spacing-micro"}).find("span", attrs={"class":"a-offscreen"})),
        "amz_buy_box": buy_box,
        "amz_seller": SellScraperLib.handle_none_attr(product_data.find("span", attrs={"class":"a-size-small offer-display-feature-text-message"})),
        "amz_dispatch": SellScraperLib.handle_none_attr(product_data.find("div", attrs={"class":"offer-display-feature-text a-spacing-none"}).find("span")),
        #"customer_reviews": product_additional_information.find("div", attrs={"id":"averageCustomerReviews"}).find("span", attrs={"class":"reviewCountTextLinkedHistogram noUnderline"})["title"],
        #"global_reviews": SellScraperLib.handle_none_attr(product_additional_information.find("span", attrs={"id":"acrCustomerReviewText"})),
        #"best_sellers_rank": SellScraperLib.handle_none_attr(product_additional_information.find_all("td")[2].find("span").find("span")),
        "amz_image": product_data.find("div", attrs={"class":"imgTagWrapper"}).find("img")["src"],
        "amz_link": product_link,
    }

    print(details)
    print("================================================================")

get_amz_product_data("https://www.amazon.co.uk/Hail-Thief-VINYL-Radiohead/dp/B01F0XNO2C/ref=sr_1_9?dib=eyJ2IjoiMSJ9.8HVWT8naoD30gkuVKIa-BfQg0NUFtzMXvnJIFWO9AuOg0JMd-0yBQVYQ0xdCWABTXye8i5NjH9CfSDolMJkhEJ8KjZsOeTWjmw4yUeaqkJtui2X7Y_NNeUqYczn8anBq_dZVRIqhrtWdTPoPiVF-C5xf_T4VUAQMhG2VRfchR-ciHKncF5Y47oPfqujH40v9xjroysZSyggHQmTMqzvMYg38263CElTc8HiZQJeHF2g.dOedJD4yIT-33JnfwMSWh_pluyypq_wzbrDX5FYCQhI&dib_tag=se&keywords=radiohead+the+bends+vinyl&qid=1709840674&sr=8-9")

