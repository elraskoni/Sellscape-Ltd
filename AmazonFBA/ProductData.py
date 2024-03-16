# Scraping Imports
import MatchProducts, SellScraperLib
import concurrent.futures
import math
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def get_ebay_categories():
    all_category_link = "https://www.ebay.co.uk/n/all-categories"
    scraped_minor_categories = []
    scraped_large_categories = []
    res_all_categories = SellScraperLib.open_page(all_category_link)
    res_big_categories = res_all_categories.find_all("h2", attrs={"class":"ttl"})
    res_small_categories = res_all_categories.find_all("a", attrs={"class":"cat-url"})

    for small_cat in res_small_categories:
        scraped_minor_categories.append(small_cat.get_text())

    for large_cat in res_big_categories:
        scraped_large_categories.append(large_cat.get_text())
    
    return (scraped_large_categories, scraped_minor_categories)


def get_product_data(scrape_link, product_limit):
    ebay_product_batch = {}  # Initialize the dictionary to store all product dictionaries
    print("================================================================")
    res_all_products = SellScraperLib.open_page(scrape_link)
    batch_count = 0
    product_results = res_all_products.find_all("div", attrs={"class":"s-item__wrapper clearfix"})
    product_count = 0


    for item in product_results:
        product_count = product_count + 1
        if product_count <= product_limit:
            product = {
                "batch_id": str(batch_count),
                "title": SellScraperLib.handle_none_attr(item.find("div", attrs={"class", "s-item__title"})),
                "price": SellScraperLib.handle_none_attr(item.find("span", attrs={"class":"s-item__price"})),
                "postage": SellScraperLib.handle_none_attr(item.find("span", attrs = {"class": "s-item__shipping s-item__logisticsCost"})),
                "seller_info":SellScraperLib.handle_none_attr(item.find("span", attrs={"class": "s-item__seller-info-text"})),
                "image": item.find("div", attrs={"class":"s-item__image-wrapper"}).find("img")["src"],
                "link": item.find("a", attrs={"class":"s-item__link"})["href"]
            }
            if product["title"] != "Shop on eBay":
                if ("New listing" in product["title"]):
                    product["title"] = product["title"].replace("New listing", "")
                batch_count = batch_count + 1
                ebay_product_batch[batch_count] = product
                print(product)

    MatchProducts.match_ebay_to_amazon(ebay_product_batch)



def search_ebay(search_params):
    for search_term_details in search_params:
        term = search_params[search_term_details]
        search_term = term["search_term"]
        search_product_limit = term["product_limit"]

        pagination_limit = (search_product_limit/240)
        pagination_limit = math.ceil(pagination_limit)

        scrape_link = SellScraperLib.build_ebay_link(search_term)
        if pagination_limit > 1:
            for page in range(1, (pagination_limit + 1)):
                scrape_link = (scrape_link + "&_pgn=" + str(page))
                get_product_data(scrape_link, search_product_limit)
        else:
            get_product_data(scrape_link,search_product_limit)


def get_search_link():
    search_link = "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw="
    return search_link

def runScraper():
    search_params = SellScraperLib.get_search_paramters()
    #large_categories, small_categories = get_ebay_categories()
    search_ebay(search_params)
