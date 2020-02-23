import sys
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import pandas as pd

data = pd.DataFrame(columns=["rating", "text"])

driver = webdriver.Firefox()

num = 132293

try:
    while True:
        num += 1

        driver.get(f"https://www.ivi.ru/watch/{num}/reviews")

        if "страница не найдена" in driver.title.lower():
            print(".", end="")
            continue
        else:
            print(num)
            while True:
                try:
                    elem = driver.find_element_by_class_name("movie-extras__nbl-button_show-more")
                    elem.click()
                except NoSuchElementException:
                    break

            elems = driver.find_elements_by_class_name("clause__toggle")
            for elem in elems:
                elem.click()

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

                data = data.append([{"rating": rating, "text": text}], ignore_index=True)

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