# A program to check Avature for duplicates
# Written by Gerald Sears 2/14/17
# Gerald Sears gesears@cisco.com
# Takes a simple csv file as input first column for lead names, and second for search criteria
# *The program expects column headers so input starts at line 2 of the input_file csv.*
# Search criteria could be url or email should be unique to each lead
# Output is a csv with name, search criteria, and output depending on if the search criteria was found in Avature.

# I removed the information for Avature's instance just to be safe upon uploading to repository.

import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver

input_file = 'searchList.csv' # path and name for input file
startRow = 1 # The first row that contains data to check in the input_file
output_file = 'found.csv' # path and name for output file
driver = webdriver.Firefox() # which webdriver for Selenium to use
waitT = 1 # How long to wait in seconds between getting one item and the next
countTo = 30 # How many seconds to wait to enter username and password into Avature window
instanceAvature = '' # <--Put your Avature instance here don't forget the trailing /
searchString = '#Search/Type: "all", In: "everything"/' # This is the string for the search settings here

# Load input file
with open(input_file, 'rt') as fin:
    cin = csv.reader(fin)
    searchFile = [row for row in cin]

# Setup Output
target_file = open(output_file, 'w+', encoding='utf-8', newline='')
outputwriter = csv.writer(target_file, dialect='excel')

# Opens login page and waits with a countdown for user to enter login information to the page directly.
driver.get('https://ciscorecruiting.avature.net/')
for i in range(1, countTo):
    print(i)
    time.sleep(1)


def getPage(target): #Function to get each search page.  Returns page as a BeautifulSoup object.
    driver.get(instanceAvature + searchString + target)
    delay = 1
    attempts = 0
    stopAfter = 10
    htmlpage = driver.page_source
    bsObj = BeautifulSoup(htmlpage, 'html.parser')
    s = bsObj.find('div', {'class':'RecentSearchItem'})
    # Logic checks to make sure the new search page has loaded by checking the search term on the page.
    # If the search term on the page doesn't match the term currently searched for it waits and checks again.
    while attempts <= stopAfter:
        if target in s.text:
            print("Page Loaded!")
            break
        time.sleep(delay)
        print("Waiting to load...")
        htmlpage = driver.page_source
        bsObj = BeautifulSoup(htmlpage, 'html.parser')
        s = bsObj.find('div', {'class': 'RecentSearchItem'})
        if attempts == stopAfter:
            print("Page Time Out: Did not load in time.")
        attempts +=1
    return bsObj

row = startRow
while row < len(searchFile):
    checkName = searchFile[row][0]
    checkTarget = searchFile[row][1]
    print('Getting ' + checkTarget + ", which is " + str(row) + ' of ' + str(len(searchFile) - startRow))
    if checkTarget == '': # Check to make sure there is something to search for this row.
        checkResults = 'No Search Provided.'
    else: # Check to see if the No Results Message is found on the page.
        pageObj = getPage(checkTarget)
        test = pageObj.find('div', {'class':'uicore_list_NoResultsMessage'})
        if test == None: # If "NoResultsMessage is not found, then the search term is in Avature
            checkResults = 'Found in system. Probable Duplicate.'
        else: # If NoResultsMessage is found then the term is not in Avature
            checkResults = 'Not found in system.'
    outputwriter.writerow([checkName,checkTarget,checkResults])
    time.sleep(waitT)
    row +=1