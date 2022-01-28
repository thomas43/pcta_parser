# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from requests import request, Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

import undetected_chromedriver.v2 as uc
import time

import sms


def open_day(month: str, days: list, open_days: list):
    count = 1
    open_day_exists = False
    for day in days:
        if day != "50":
            print("Got a " + month + " day: " + str(count))
            open_days.append(month + " " + str(count))
            open_day_exists = True
        count = count + 1

    return open_day_exists


def parse(driver):

    try:
        # Landing Page
        driver.get('https://permit.pcta.org/application')
        time.sleep(2)

        # Sometimes it brings you to the start permit process page, without cookies?
        continue_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/a')
        continue_button.click()
        time.sleep(2)

        # Click Continue Button
        continue_button = driver.find_element(By.XPATH, '//*[@id="permit-form"]/div/div')
        continue_button.click()
        time.sleep(2)
        # driver.get_screenshot_as_file('test.png')


        # Select a Start Location (Has to be first)
        start_location_dropdown = driver.find_element(By.ID, 'start_location_id')
        start_select = Select(start_location_dropdown)
        start_select.select_by_value("1")  # Mexico Border
        time.sleep(1)

        # Select an End Location (Had to be last)
        end_location_dropdown = driver.find_element(By.ID, 'end_location_id')
        end_select = Select(end_location_dropdown)
        end_select.select_by_value("116")  # Canadian Border
        time.sleep(1)

        # Click Continue Button
        continue_button = driver.find_element(By.XPATH, '//*[@id="permit-form"]/div[4]/div[1]')
        continue_button.click()
        time.sleep(2)

        # Get all Days in March
        row1xp = '//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[2]/table/tbody/tr'
        row2xp = '//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/div[2]/table/tbody/tr'
        row3xp = '//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[3]/div[2]/table/tbody/tr'
        row4xp = '//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[4]/div[2]/table/tbody/tr'
        row5xp = '//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[5]/div[2]/table/tbody/tr'
        row6xp = '//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[6]/div[2]/table/tbody/tr'

        row_xpaths = list()
        row_xpaths.append(row1xp)
        row_xpaths.append(row2xp)
        row_xpaths.append(row3xp)
        row_xpaths.append(row4xp)
        row_xpaths.append(row5xp)
        row_xpaths.append(row6xp)

        march_days = list()
        april_days = list()
        may_days = list()

        # Get all days in March Calendar
        for row_xpath in row_xpaths:
            row = driver.find_element(By.XPATH, row_xpath)
            nums = row.find_elements(By.CLASS_NAME, "fc-title")
            for num in nums:
                #print(repr(num))
                #print(num.text)
                march_days.append(num.text)

        print(len(march_days))

        # Get all days in April Calendar

        next_month_button = driver.find_element(By.XPATH, '//*[@id="calendar"]/div[1]/div[3]/div/button[2]')
        next_month_button.click()
        time.sleep(2)

        for row_xpath in row_xpaths:
            row = driver.find_element(By.XPATH, row_xpath)
            nums = row.find_elements(By.CLASS_NAME, "fc-title")
            for num in nums:
                #print(repr(num))
                #print(num.text)
                april_days.append(num.text)

        print(len(april_days))

        # Get all days in May Calendar

        next_month_button = driver.find_element(By.XPATH, '//*[@id="calendar"]/div[1]/div[3]/div/button[2]')
        next_month_button.click()
        time.sleep(2)

        for row_xpath in row_xpaths:
            row = driver.find_element(By.XPATH, row_xpath)
            nums = row.find_elements(By.CLASS_NAME, "fc-title")
            for num in nums:
                # print(repr(num))
                # print(num.text)
                may_days.append(num.text)

        print(len(may_days))
        driver.delete_all_cookies()
        driver.quit()

        dates = {
            'March': march_days,
            'April': april_days,
            'May': may_days

        }
        return dates

    except Exception as e:
        print("!!! Got an exception: " + str(e))
        return dict()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    options = uc.ChromeOptions()
    options.headless = False

    driver = uc.Chrome(options=options)
    attempts = 1
    while True:
        print("Parsing attempt: " + str(attempts))
        month_day_dict = parse(driver)
        for month in month_day_dict:
            open_days = []
            if open_day(month, month_day_dict[month], open_days):
                print("!!! Got at least one open day!")
                text = "The following day(s) are open: "
                for day in open_days:
                    text += day
                    text += ", "
                sms.send(text)

        time.sleep(120)  # Rerun loop every 2 minutes.
        attempts = attempts + 1


