#coding:utf-8
# Alex Xudong Sun 2/11/2019


from selenium import webdriver
from time import sleep
from nltk import ngrams
from collections import Counter
import requests
from bs4 import BeautifulSoup
import string
import re
import random
import pandas as pd
import matplotlib.pyplot as plt

# install chromedriver firstly
# start a driver/let this script "use" the browser

def SearchOneKeyword(keyword, starturl = "http://news.mit.edu/"):
    driver = webdriver.Chrome(r'C:\Program Files\Python37\chromedriver.exe')
    # the page that has a search bar
    driver.get(starturl)

    # search text test
    driver.find_element_by_id('keyword').send_keys(keyword)
    # search button
    driver.find_element_by_id('submit-search').click()

    # the outcome url
    url = driver.current_url
    # all results
    content = requests.get(url)
    soup = BeautifulSoup(content.content, "html.parser")

    count = soup.find("div", attrs = {"class":"view-header"}).text

    num_show = int(re.search(r'-(.*?)of', count).group(1))
    num_result = int(re.search(r'of(.*?)Results', count).group(1))


    # first-page results
    articles = soup.find_all("h3", attrs={"class": "title"})
    deks = soup.find_all("p", attrs={"class": "dek"})
    dates = soup.find_all("em", attrs={"class": "date"})

    num_viewed = len(articles)


    # loop through all other pages
    while num_viewed < num_result:
        # next page
        print('proceed to next page')
        next_page = starturl  + soup.find('a', attrs = {'title':'Go to next page'})['href']
        sleep(random.randrange(2,10))
        driver.get(next_page)
        new_content = requests.get(driver.current_url)
        soup = BeautifulSoup(new_content.content, "html.parser")

        new_articles = soup.find_all("h3", attrs={"class": "title"})
        articles += new_articles
        deks += soup.find_all("p", attrs={"class": "dek"})
        dates += soup.find_all("em", attrs={"class": "date"})

        num_viewed += len(new_articles)

        print('get ' + str(num_viewed) + ' results')
        sleep(random.randrange(2,10))


    if len(articles) != len(dates):
        raise ValueError('articles and dates not match')


    l_one_keyword = []
    for i in range(len(articles)):
        title = articles[i].text
        link = starturl + articles[i].find('a', href = True)['href']
        dek = deks[i].text
        date = dates[i].text
        l_one_keyword.append({'id_article':i, 'title':title, 'link':link, 'dek':dek, 'date':date})

    return l_one_keyword

# test1 = SearchOneKeyword('3D printing')
#
# test1
#
#
# df_test = pd.DataFrame(test1)
#
# df_test
#
# df_test['date'] = pd.to_datetime(df_test['date'])
#
# # pd.DataFrame(df_test['id_article'].groupby([df_test["date"].dt.year]).count()).plot(kind="bar")
#
# df_keyword = df_test
# df_yearcount = df_keyword['id_article'].groupby(df_keyword['date'].dt.year).count()
#
# df_yearcount = pd.DataFrame(df_yearcount.reset_index())
# df_yearcount
# df_plot = pd.DataFrame({'time': range(2000,2019)})
# df_plot
# df_plot.columns = ['year']
#
# df_merged = df_plot.merge(df_yearcount, how = 'left', left_on = 'year', right_on = 'date')
# df_merged_plot = df_merged.drop(columns=['date']).fillna(0)
# df_merged_plot
# plt.plot('year','id_article', data = df_merged_plot, marker='o', markerfacecolor='blue', markersize=8, color='skyblue', linewidth=2)

# search a list of keywords
keywords_l = ['3D printing', 'graphene', 'IOT', 'nanotubes', 'robotics', 'blockchain', 'drones', 'AR']


df_onekeyword_l = []

df_allplots = pd.DataFrame({'time': range(2000,2019)})
df_allplots.columns = ['year']

for keyword in keywords_l:
    # keyword = '4D printing'
    colname_keyword = 'count_' + str(keyword)

    df_keyword = SearchOneKeyword(keyword)

    df_onekeyword_l.append(df_keyword)

    df_keyword = pd.DataFrame(df_keyword)
    df_keyword['date'] = pd.to_datetime(df_keyword['date'])
    df_yearcount = df_keyword['id_article'].groupby(df_keyword['date'].dt.year).count()

    df_yearcount = pd.DataFrame(df_yearcount.reset_index())

    df_yearcount.columns = ['date', colname_keyword]


    df_plot = pd.DataFrame({'time': range(2000,2019)})
    df_plot.columns = ['year']

    df_allplots = df_allplots.merge(df_yearcount, how = 'left', left_on = 'year', right_on = 'date')
    df_allplots = df_allplots.drop(columns=['date']).fillna(0)

# df_allplots

legend_l = []
for keyword in keywords_l:
    colname_keyword = 'count_' + str(keyword)
    plt.plot('year',colname_keyword, data = df_allplots, marker='o', markersize=4, linewidth=1)
    legend_l.append(str(keyword))

plt.legend(legend_l, loc='upper left')
plt.show()
