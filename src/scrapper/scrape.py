from selenium import webdriver
from selenium.webdriver.common.by import By
from src.exception import CustomException
from bs4 import BeautifulSoup as bs
import pandas as pd
import os, sys
import time
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote, urljoin


class ScrapeReviews:
    def __init__(self, product_name: str, no_of_products: int):
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.product_name = product_name
        self.no_of_products = no_of_products

    def scrape_product_urls(self, product_name):
        try:
            search_string = product_name.replace(" ", "-")
            encoded_query = quote(search_string)
            self.driver.get(
                f"https://www.myntra.com/{search_string}?rawQuery={encoded_query}"
            )
            myntra_text = self.driver.page_source
            myntra_html = bs(myntra_text, "html.parser")
            pclass = myntra_html.findAll("ul", {"class": "results-base"})

            product_urls = []
            for i in pclass:
                href = i.find_all("a", href=True)
                for product_no in range(len(href)):
                    t = href[product_no]["href"]
                    product_urls.append(t)
            return product_urls
        except Exception as e:
            raise CustomException(e, sys)

    def extract_reviews(self, product_link):
        try:
            productLink = urljoin("https://www.myntra.com", product_link)
            self.driver.get(productLink)
            prodRes = self.driver.page_source
            prodRes_html = bs(prodRes, "html.parser")
            title_h = prodRes_html.findAll("title")
            self.product_title = title_h[0].text

            overallRating = prodRes_html.findAll("div", {"class": "index-overallRating"})
            for i in overallRating:
                self.product_rating_value = i.find("div").text

            price = prodRes_html.findAll("span", {"class": "pdp-price"})
            for i in price:
                self.product_price = i.text

            product_reviews = prodRes_html.find("a", {"class": "detailed-reviews-allReviews"})
            if not product_reviews:
                return None
            return product_reviews
        except Exception as e:
            raise CustomException(e, sys)

    def scroll_to_load_reviews(self):
        self.driver.set_window_size(1920, 1080)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def extract_products(self, product_reviews, product_url):
        try:
            t2 = product_reviews["href"]
            Review_link = urljoin("https://www.myntra.com", t2)
            Product_link = urljoin("https://www.myntra.com", product_url)

            self.driver.get(Review_link)
            self.scroll_to_load_reviews()
            review_page = self.driver.page_source
            review_html = bs(review_page, "html.parser")
            review = review_html.findAll("div", {"class": "detailed-reviews-userReviewsContainer"})

            for i in review:
                user_rating = i.findAll("div", {"class": "user-review-main user-review-showRating"})
                user_comment = i.findAll("div", {"class": "user-review-reviewTextWrapper"})
                user_name = i.findAll("div", {"class": "user-review-left"})

            reviews = []
            max_reviews = min(5, len(user_rating))
            for i in range(max_reviews):
                try:
                    rating = user_rating[i].find("span", class_="user-review-starRating").get_text().strip()
                except:
                    rating = "No rating Given"
                try:
                    comment = user_comment[i].text
                except:
                    comment = "No comment Given"
                try:
                    name = user_name[i].find("span").text
                except:
                    name = "No Name given"
                try:
                    date = user_name[i].find_all("span")[1].text
                except:
                    date = "No Date given"

                mydict = {
                    "Product Name": self.product_title,
                    "Product Link": Product_link,
                    "Over_All_Rating": self.product_rating_value,
                    "Price": self.product_price,
                    "Date": date,
                    "Rating": rating,
                    "Name": name,
                    "Comment": comment,
                }
                reviews.append(mydict)

            review_data = pd.DataFrame(reviews, columns=[
                "Product Name", "Product Link", "Over_All_Rating",
                "Price", "Date", "Rating", "Name", "Comment",
            ])
            return review_data
        except Exception as e:
            raise CustomException(e, sys)

    def get_review_data(self) -> pd.DataFrame:
        try:
            product_urls = self.scrape_product_urls(product_name=self.product_name)
            product_urls = list(dict.fromkeys(product_urls))  # unique only

            product_details = []
            scraped_count = 0
            for product_url in product_urls:
                if scraped_count >= self.no_of_products:
                    break
                review = self.extract_reviews(product_url)
                if review:
                    product_detail = self.extract_products(review, product_url)
                    product_details.append(product_detail)
                    scraped_count += 1

            self.driver.quit()
            if not product_details:
                return pd.DataFrame()

            data = pd.concat(product_details, axis=0)
            data.to_csv("data.csv", index=False)
            return data
        except Exception as e:
            self.driver.quit()
            raise CustomException(e, sys)