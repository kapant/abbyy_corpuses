# before start: export PATH=$PATH:/data/kapant/geckodriver

import sys
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

import pandas as pd

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

num = 117870

try:
    while True:
        num += 1
        
        # getting reviews page
        driver.get(f"https://www.ivi.ru/watch/{num}/reviews")
        
        # check if it exist
        if "страница не найдена" in driver.title.lower():
            print(str(num) + " not found")
            continue
        else:
            print(str(num) + " exists")
            data = pd.DataFrame(columns=["rating", "title", "text"])
            
            title = driver.title.replace("Рецензии на фильм ", "")
            title = title.replace("Рецензии на мультфильм ", "")
            
            # show all reviews
            while True:
                try:
                    elem = driver.find_element_by_class_name("movie-extras__nbl-button_show-more")
                    elem.click()
                except NoSuchElementException:
                    break
            
            # show whole entry of each review
            elems = driver.find_elements_by_class_name("clause__toggle")
            for elem in elems:
                elem.click()

            # extracting text and rating
            reviews = driver.find_elements_by_class_name("movie-extras__item")
            for review in reviews:
                try:
                    rating = review.find_element_by_xpath('.//div[@class="movie-extras__item-rating"]').text
                except NoSuchElementException:
                    rating = None

                try:
                    text = review.find_element_by_xpath(".//p").text
                except NoSuchElementException:
                    continue

                data = data.append([{"rating": rating, "title": title, "text": text}], ignore_index=True)

            if len(data["rating"]) > 0:
                data.to_csv(f"./reviews/movie_{num}.csv", encoding="utf-8", index=False)

    driver.close()
except KeyboardInterrupt:
    with open("./last_number.txt", "w") as f:
        f.write(str(num))
        f.close()
    print(f"\nLast number: {num}\n")
    driver.close()
    
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
except Exception as e:
    print(e)
    with open("./last_number.txt", "w") as f:
        f.write(str(num))
        f.close()
    print(f"\nLast number: {num}\n")
    driver.close()
    
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
