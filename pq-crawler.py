## !/usr/bin/python

from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
import os

 
# Set initial URL and storage path
mainurl = 'https://url-path-from-proquest/'
storagepath = '/path-to-main-folder/'

# Setup for urls in case of relative links
parts = urlsplit(mainurl)
base_url = '{0.scheme}://{0.netloc}'.format(parts)
path = mainurl[:mainurl.rfind('/')+1] if '/' in parts.path else mainurl

#Obtain main list of links (i.e. main page sent to us by PQ)
try:
    mainlist = requests.get(mainurl)
except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
    print('Main URL is not responding or is incorrect')
mainpage = BeautifulSoup(mainlist.text, 'lxml')
mainpagelinks = []

#Extracting main links from main page
for anchor in mainpage.find_all('a'):        
    link = anchor.attrs['href'] if 'href' in anchor.attrs else ''  # extract link url from the anchor and confirming that <a> has an actual url
    # Accounting for any relative links
    if link.startswith('/'):
        link = base_url + link
    elif not link.startswith('http'):
        link = path + link
    # add the new url to the list
    if not link in mainpagelinks:
        mainpagelinks.append(link)

# Failsafe to make sure we don't pull a subpage or document link twice
processed_urls = set()

# Container for any 400 or 500 responses from doc download attempts:
failed_download = []
  
# Start subpage and document pulling process

doccount = 0
for sublink in mainpagelinks:  #set to mainpagelinks[:1] to test just 1 first
    if not os.path.exists(storagepath + 'FOLDER_STRING/'):   #A folder should be created for each page of links
        os.makedirs(storagepath + 'FOLDER_STRING/')                 #Folder name should be based on page/link id
    try:                                                    #We will need to find out PQ's organization of IDs to extract this folder name from URL
        if not sublink in processed_urls:
            response = requests.get(sublink)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        continue
    subpage = BeautifulSoup(response.text, 'lxml')  #Pull the subpage containing doc links
    
    #Iterate through all hyperlinks (i.e. doc links) in the subpage
    
    for anchor in subpage.find_all('a'):     #set to subpage.find_all('a')[:1] to test just first link
        link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
        # Accounting for any relative links
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        print('Attempting to process: ', link)  #Now we hit the xml doc link directly
        try:
            if not link in processed_urls:
                docxml = requests.get(link)
                if docxml.status_code == 200:
                    doccount+=1                      
                        #Assuming we'll want to make a doc named based on an id in the anchor contents
                    with open(storagepath + 'FOLDER_STRING/' + anchor.string.replace(' ','_') + '.xml', 'w') as file:
                        file.write(docxml.text)
                        file.close()
                else:
                    failed_download.append(link)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
            continue
        processed_urls.add(link)
    processed_urls.add(sublink)    
    
    
print('Complete: ', doccount, ' documents; ', len(failed_download), ' requests turned down.')    
    