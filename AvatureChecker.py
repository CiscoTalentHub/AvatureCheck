# A program to check Avature for duplicates
# Written by Gerald Sears 2/14/17
# Gerald Sears gesears@cisco.com
# Takes a simple csv file as input first column for lead names, and second for search criteria
# *The program expects column headers so input starts at line 2 of the input_file csv.*
# Search criteria could be url or email should be unique to each lead
# Output is a csv with name, search criteria, and output depending on if the search criteria was found in Avature.
# **To get this working you need to put .config.ini under MyDocuments\AvatureChecker**
# I plan to add code to do this automatically but haven't gotten there yet.

# TODO Add a UI look into cli first then gui
# TODO Saved checked terms to file or database to use as a pre-check.
#      Only saved those terms found in Avature.
# TODO Find and impliment a good error/debugging/testing setup.  Print statements might not be enough
# TODO Add logic to allow multi-value checking(eg Name AND location or Name AND Employer)

import csv
import time
import os
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver

# Loading settings and learning about the system
userHome = os.path.expanduser('~')  # Gets the home folder location for the user
if os.name == 'nt':
    checkerDir = userHome + '\\Documents\\AvatureChecker\\'
elif os.name == 'posix':
    checkerDir = userHome + '/AvatureChecker/'
else:
    print("Sorry, unfamiliar with this sytem please set pathnames manually.")
    checkerDir = '.'
# Checking to see if the AvatureCheck directory exists, if not creates one.
if os.path.exists(checkerDir):
    print("Loading from " + checkerDir)
else:
    os.system('mkdir ' + checkerDir)
    # TODO Add code to install a default .config.ini upon first startup
cfglocation = checkerDir + '.config.ini'
cfg = configparser.ConfigParser()
cfg.read(cfglocation)
input_file = checkerDir + cfg['inputset']['input_Name']  # path and name for input file
startRow = int(cfg['inputset']['firstLine'])  # The first row that contains data to check in the input_file
output_file = checkerDir + cfg['outputset']['output_Name']  # path and name for output file
keephead = cfg['outputset']['keepHead']  # Sets if you want to keep headings from the input file
# TODO Add logic to allow the webdriver to be set in the configuration file
driver = webdriver.Firefox()
waitT = float(cfg['waitset']['waitT'])  # How long to wait in seconds between getting one item and the next
countTo = int(cfg['loginset']['countTo'])  # How many seconds to wait to enter username and password into Avature window
instanceAvature = cfg['Avatureset']['instanceAvature']  # <-Put your Avature instance here don't forget the trailing /
print(instanceAvature)
searchString = cfg['Avatureset']['searchString']  # This is the string for the search settings here
print(instanceAvature + searchStr

# Load input file
with open(input_file, 'rt', encoding='utf-8') as fin:
    cin = csv.reader(fin)
    searchFile = [row for row in cin]
    print(searchFile)

# Setup Output
def start_csvout(output):  # Creates a new csv file for output. Overwrites existing file, if any!
    target_file = open(output, 'wt', encoding='utf-8', newline='')
    return csv.writer(target_file, dialect='excel')


# Opens login page and waits with a countdown for user to enter login information to the page directly.
# TODO Add logic to check to see if the page is logged-in instead of waiting for countdown
def loginAvature(count): #Initial Avature Login
    driver.get(instanceAvature)
    for i in range(1, count):
        print(count - i)
        time.sleep(1)


# Function to get each search page.  Returns page as a BeautifulSoup object.
def getPage(target):
    driver.get(instanceAvature + searchString + target)
    delay = 1.5
    attempts = 0
    stopAfter = 5
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
            bsObj = False
        attempts +=1
    return bsObj

loginAvature(countTo)
row = startRow
outputwriter = start_csvout(output_file)
while row < len(searchFile):
    print('row is ' + str(row))
    print('len searchfile is ' + str(len(searchFile)))
    checkName = searchFile[row][0]
    checkTarget = searchFile[row][1]
    print('Checking ' + checkTarget + ", which is " + str(row) + ' of ' + str(len(searchFile) - startRow))
    # TODO Put test logic into its own function
    if checkTarget == '':  # Check to make sure there is something to search for this row.
        checkResults = 'No Search Provided.'
    else:  # Check to see if the No Results Message is found on the page.
        pageObj = getPage(checkTarget)
        if pageObj == False:
            checkResults = 'System Timed Out.'
        else:
            test = pageObj.find('div', {'class':'uicore_list_NoResultsMessage'})
            if test == None:  # If "NoResultsMessage is not found, then the search term is in Avature
                checkResults = 'Found in system. Probable Duplicate.'
            else:  # If NoResultsMessage is found then the term is not in Avature
                checkResults = 'Not found in system.'

    outputwriter.writerow([checkName, checkTarget, checkResults])
    time.sleep(waitT)
    row += 1