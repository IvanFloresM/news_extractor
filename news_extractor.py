# requests is for making web requests.
# It helps us download webpages.
import requests

# bs4 is the name of BeautifulSoup.
# BeautifulSoup is for parsing websites.
from bs4 import BeautifulSoup

# time is a package to manage pauses and waits.
import time

# pandas is used for managing CSVs.
import pandas as pd

# newspaper is a library for extracting new´s articles
from newspaper import Article

# numpy is used for matrix algebra
import numpy as np

# base for is used for decoding strings
import base64

# streamlit is used to build web app for data science projects. 
import streamlit as st
        
##################################################

### Create Header
st.title("News Extractor")

# Instructions
st.write("Paste the URLs of the news articles you want to download in the text box. Separate the articles´ links with a comma. Do not add space after the comma.")

# Create text cell
urls = st.text_area('Articles´ links to scrape', height = 100)
## Now we will scrape the content of all the stories we found.

# Remove last character from string
links = urls[:-1]

# Convert string to list
links = links.split(",")

###########################################

# Create empty list
story_data = []

#Assign time.time() object to "start" so we can profile the code.
start = time.time()

#Intialize list articles_info list
articles_info = []
content = []

#Loop through items in list
for i in links:

    try:
        #Intialize dictionary  
        article_dict = {}
        
        #Insert link "i" into the dictionary
        #Pass link into Article() function
        art = Article(i, language="en")
        
        #Download contents of art object
        art.download()
        
        #And summary into corresponding keys
        art.parse()
        article_dict["text"] = art.text
        content.append(art.text)
        article_dict["title"] = art.title
        article_dict["author"] = art.authors
        article_dict["date"] = art.publish_date
        art.nlp()
        
        # Insert dictionary of article info into the articles_info list
        articles_info.append(article_dict)
        
        # Pass the list of dictionaries into a pandas data frame
        corpus = pd.DataFrame(articles_info)
        
        # Print how long the process took
        print("Script took {:.2f} seconds to complete".format(time.time() - start))
    
    # Add excemption to loop
    except:
        pass


# Print articles´ metadata
st.header("Article's metadata")
st.write(corpus)

# Create download button for news articles dataframe
csv = corpus.to_csv().encode()
b64 = base64.b64encode(csv).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="news_data.csv" target="_blank">Download csv file</a>'
st.markdown(href, unsafe_allow_html=True)

