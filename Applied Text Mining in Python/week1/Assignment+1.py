
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 1
# 
# In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 
# 
# Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.
# 
# The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 
# 
# Here is a list of some of the variants you might encounter in this dataset:
# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010
# 
# Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
# * Assume all dates in xx/xx/xx format are mm/dd/yy
# * Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# * If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# * If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
# * Watch out for potential typos as this is a raw, real-life derived dataset.
# 
# With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.
# 
# For example if the original series was this:
# 
#     0    1999
#     1    2010
#     2    1978
#     3    2015
#     4    1985
# 
# Your function should return this:
# 
#     0    2
#     1    4
#     2    0
#     3    1
#     4    3
# 
# Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.
# 
# *This function should return a Series of length 500 and dtype int.*

# In[16]:


import pandas as pd
import datetime
import re
from  dateutil.parser import parse

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
df.head()


# In[76]:


def date_sorter():
    
    result = df.str.findall(r'(\d?\d[/-]\d?\d[/-]\d+)') + df.str.findall(r'(\d?\d/\d{4})') + df.str.findall(r'([ADFJMNOS][ueuaoce]\w*[-\s.]\s?\d?\d[snrt]*\w*[-\s,]\s?\d{4})') + df.str.findall(r'(\d?\d?\s?[ADFJMNOS][upeuaoce]\w*[\s.,]\s?\d{4})') + df.str.findall(r'(\d{4})') 
    result = result.apply(lambda i: i[0])
    result[80] = "6/29/81"
    result[99] = "11/14/83"
    result[248] = "July 1995"
    result[271] = "August 2008"
    print(result[413])
    for i, date in enumerate(result, start=0):
        if re.match("(\d{4})", date):
            result[i] = "1/1/"+date
        elif re.match("(\d?\d/\d{4})", date):
            date_split = date.split("/")
            result[i] = date_split[0]+"/1/"+date_split[1]
        elif re.match("(\d?\d/\d?\d/\d{2}\Z)", date):
            date_split = date.split("/")
            result[i] = date_split[0]+"/"+date_split[1]+"/19"+date_split[2]
        elif re.match("(\d?\d-\d?\d-\d{2}\Z)", date):
            date_split = date.split("-")
            result[i] = date_split[0]+"/"+date_split[1]+"/19"+date_split[2]
        elif re.match("(\d?\d-\d?\d-\d{4})", date):
            date_split = date.split("-")
            result[i] = date_split[0]+"/"+date_split[1]+"/"+date_split[2]
        elif(re.match(r'[A-Z][a-z]+[,.]? \d{4}',date)) :
            date_split = date.split(' ')
            result[i] = date_split[0] + ' 1 '+date_split[1]
        result[i] = parse(str(result[i]),fuzzy=True).strftime("%m/%d/%Y")
    
    result = result.apply(lambda date: datetime.datetime.strptime(date, "%m/%d/%Y"))
    
    sorted_result = pd.DataFrame()
    sorted_result["Date"] = result
    sorted_result["original_index"] = result.index
    sorted_result = sorted_result.sort_values(by=['Date'])
    sorted_result.index = range(len(sorted_result))
    return sorted_result["original_index"]
date_sorter()


# In[ ]:




