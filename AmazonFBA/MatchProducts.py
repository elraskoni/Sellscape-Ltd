# Scraping Imports
import Levenshtein
import SellScraperLib
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def match_ebay_to_amazon(ebay_products_batch):
    matched_listings_batch = []

    for ebay_product_key in range(1, len(ebay_products_batch) + 1):
        ebay_product = ebay_products_batch[ebay_product_key]
        ebay_product_title = ebay_product["title"]

        print("calling amz with title:" + ebay_product_title)
        amazon_listings = SellScraperLib.get_amazon_listings(ebay_product_title)  # Call scrape_listings for each eBay product
        matched_listings = []
    
        for amazon_listing in amazon_listings:
            print(amazon_listing)
            # Compare product titles
            title_similarity = calculate_similarity(ebay_product['title'], amazon_listing['title'])

            # Define a threshold for similarity
            threshold = 0.5  # Adjust as needed
            
            # If the overall similarity exceeds the threshold, consider it a match
            if title_similarity >= threshold:
                matched_listings.append({
                    'ebay_product': ebay_product,
                    'amazon_listing': amazon_listing,
                    'similarity_score': title_similarity
               })
        
        matched_listings_batch.append(matched_listings)
    
    return matched_listings_batch


def calculate_similarity(input_string, string_list):
    best_match_l = None
    best_score_l = 0

    for string in string_list["amz_title"]:
        score_l = Levenshtein.ratio(input_string, string)

        if score_l > best_score_l:
            best_score_l = score_l
            best_match_l = string

    print("match string with: ")
    print(str(input_string))
    print("================================================")
    print(" Levenshtien best match : ")
    print(str(best_match_l))
    print(" Leventshtien best score : " + str(best_score_l))
    print("================================================")

    #return best_match, best_score  # Return the best match and the best score
