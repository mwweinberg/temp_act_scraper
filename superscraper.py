# -*- coding: utf-8 -*-

import urllib
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
from lxml import html

import time
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

#for the reconcile
import csv

#creates the output list
output_csv_list = []


browser_mps = webdriver.Chrome('chromedriver')
mps_url = "http://ngo.mps.gov.cn/ngo/portal/toInfogs.do?p_type=1"
browser_mps.get(mps_url)


element = WebDriverWait(browser_mps, 45).until(EC.presence_of_element_located((By.LINK_TEXT, "临时活动公示")))


browser_mps.find_elements_by_link_text('临时活动公示')[0].click()


## Getting max page for the second table:
element = WebDriverWait(browser_mps, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "r-grid-indexPage")))


### Might need to add a break before this:
browser_soup = BeautifulSoup(browser_mps.page_source,"lxml")
max_page_class = browser_soup.find_all("span", {"class":"r-grid-indexPage"})
page_count_re = re.compile('\/[   ]*?(\d*)[   ]*?页')

#MW changed max_page_class[1] to max_page_class[0] here
#Because I was getting a list index out of range error
mps_max_page_search = re.search(page_count_re,max_page_class[0].get_text().encode('utf-8'))
max_page = mps_max_page_search.group(1)


### Might need to add a break before this:
page_table_holder = []
counter = 1
#time.sleep(15)

#*******************
#*******************
#*******************
#one more than the number of pages
max_page = 3

###
while counter < int(max_page):


    element = WebDriverWait(browser_mps, 100).until(EC.presence_of_element_located((By.LINK_TEXT, "下一页")))

    attempts = 1
    while attempts < 20:

        browser_soup_temp = BeautifulSoup(browser_mps.page_source,"lxml")
        tbody_holder = browser_soup_temp.find_all("tbody")[1]
        tr_holder = tbody_holder.find_all("tr")

        td_holder = tr_holder[0].find_all("td")

        current_start_bianhao = td_holder[0].get_text()

	if counter == 1:
	    max_bianhao = int(current_start_bianhao)
	    print "max_bianhao is: " + str(max_bianhao)

        if current_start_bianhao == str( max_bianhao - (counter-1)*10):
            attempts = 20
            print "Confirmed new Bianhao, moving along"
            for tr_item in tr_holder:
                row_holder = []
                for item in tr_item.find_all('td'):
                    row_holder.append(item.get_text())
                    page_no_str = "page: " + str(counter)


                page_table_holder.append(row_holder)

        else:
            attempts += 1
            print "Same Bianhao, trying again after: ", attempts - 1
            time.sleep(3)

    print "Scraped Page: ", counter

    element = WebDriverWait(browser_mps, 100).until(EC.presence_of_element_located((By.LINK_TEXT, "下一页")))
    time.sleep(10)
    browser_mps.find_elements_by_link_text('下一页')[0].click()
    counter += 1

## Does this grab the last page?


page_table_DF = pd.DataFrame(page_table_holder)

#prints to a csv without headers and indexes
page_table_DF.to_csv('new.csv', encoding='utf-8', header=False, index=False)

#prints an archive version of the current csv
timestamp = time.strftime("%Y%m%d")
time_filename = "tempactMPS" + timestamp + ".csv"
page_table_DF.to_csv(time_filename, encoding='utf-8', header=False, index=False)

#begin what used to be reconcile
#turns csvs into lists of lists

with open('old.csv', 'rU') as f:
    reader = csv.reader(f)
    old_csv_list = list(list(rec) for rec in csv.reader(f, delimiter=','))
    #removes the ordinals that start each entry because they are not relevant and change even if the data is the same
    for element in old_csv_list:
        del element[0]
    #print(old_csv_list)

with open('new.csv', 'rU') as f:
    reader = csv.reader(f)
    new_csv_list = list(list(rec) for rec in csv.reader(f, delimiter=','))
    for element in new_csv_list:
        del element[0]
    #print(new_csv_list)

# if element is not in old list, add to output list

for element in new_csv_list:
    if element in old_csv_list:
        print('existing entry')
    else:
        print('new entry')
        output_csv_list.append(element)

for element in output_csv_list:
    #adds a blank entry to each of these spaces
    element.insert(0, '')
    element.insert(1, '')
    element.insert(2, '')
    element.insert(4, '')
    element.insert(6, '')
    element.insert(7, '')
    element.insert(9, '')
    element.insert(10, '')
    element.insert(11, '')

#pulls the start and stop dates out, fixes format, and inserts

for element in output_csv_list:
    full_date = element[13]
    first_date = full_date[:10]
    first_date_fixed = first_date.replace('.', '-')
    second_date = full_date[11:]
    second_date_fixed = second_date.replace('.', '-')
    print first_date_fixed
    print second_date_fixed

    element.insert(13, second_date_fixed)
    element.insert(13, first_date_fixed)

#output to CSV
with open('tempactdiffs.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(output_csv_list)
