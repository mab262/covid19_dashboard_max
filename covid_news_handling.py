"""A module containing the relevant functions for working with the covid news and newsapi.org"""

import json
import requests
import re


def news_API_request(covid_terms: str = "Covid COVID-19 coronavirus") -> list:
    """A function which makes an API request using the keywords as an argument"""

    covid_terms = re.sub("\s+", " OR ", covid_terms.strip())  # converts the keyword arguments into a url api request
    # friendly format

    f = open("config.json", "r")
    data = json.loads(f.read())  # accesses data from the config file

    url = ('https://newsapi.org/v2/everything?'
           'q=&'
           'language=en&'
           'apiKey={}'.format(data["API-keys"]["news"]))  # creates a url request using the covid keywords

    url = url[:36] + covid_terms + url[36:]  # inserts the keywords into the url

    response = requests.get(url)
    # creating an api request using the url

    newslist = []
    x = 0
    y = 10

    for i in range(x, y):
        temp = dict()
        if response.json()["articles"][i]["title"] not in data["removed"]["articles"]:
            temp["title"] = response.json()["articles"][i]["title"]
            temp["content"] = response.json()["articles"][i]["content"][0:150] + "..."
            newslist.append(temp)
        else:
            temp["title"] = response.json()["articles"][y]["title"]
            temp["content"] = response.json()["articles"][y]["content"][0:150] + "..."
            newslist.append(temp)
            y += 1
            x += 1

    return newslist


def update_news(title: str) -> int:
    """A function which keeps track of the removed news articles"""
    with open("config.json", 'r+') as f:
        file_data = json.load(f)
        file_data["removed"]["articles"].append(title)
        f.seek(0)
        json.dump(file_data, f, indent=4)

    print(news_API_request())  # creates a new request which will omit the article now in the removed list

    return 0


if __name__ == '__main__':
    news_API_request()
