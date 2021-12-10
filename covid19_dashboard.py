"""A module which uses the Flask module to decorate the html interface"""

import webbrowser
import timeconversion
import logging
import json
import sched
from flask import Flask, render_template, request
from covid_data_handler import parse_csv_data, process_covid_csv_data, covid_API_request, schedule_covid_updates
from covid_news_handling import news_API_request, update_news


def run():
    webbrowser.open('http://127.0.0.1:5000/')
    app.run()


app = Flask(__name__)

f = open("config.json", "r")
data = json.loads(f.read())

local_data = covid_API_request()
national_data = covid_API_request("England", "nation")

event_updates = list()


@app.route('/index')
def title():
    news_remove = request.args.getlist("notif")
    update_query_name = request.args.getlist("two")
    update_query_time = request.args.getlist("update")  # user inputs into the webpage

    if news_remove:
        article = (str(news_remove[0]))
        print(article)
        update_news(article)
        return render_template('index.html', title=data["keywords"]["title"], location=data["keywords"]["location"],
                               local_7day_infections=local_data["data"][1]["cumCasesBySpecimenDateRate"],
                               nation_location=data["keywords"]["national_location"],
                               national_7day_infections=national_data["data"][1]["cumCasesBySpecimenDateRate"],
                               hospital_cases=national_data["data"][1]["hospitalCases"],
                               deaths_total=national_data["data"][1]["cumDeaths60DaysByDeathDate"],
                               # allows the user to remove news they dont want to see

                               news_articles=news_API_request(), updates=event_updates)
    elif not news_remove and not update_query_name and not update_query_time:
        return render_template('index.html', title=data["keywords"]["title"], location=data["keywords"]["location"],
                               local_7day_infections=local_data["data"][1]["cumCasesBySpecimenDateRate"],
                               nation_location=data["keywords"]["national_location"],
                               national_7day_infections=national_data["data"][1]["cumCasesBySpecimenDateRate"],
                               hospital_cases=national_data["data"][1]["hospitalCases"],
                               deaths_total=national_data["data"][1]["cumDeaths60DaysByDeathDate"],
                               news_articles=news_API_request(), updates=event_updates)
        # allows the page to be refreshed every 30 seconds to automatically update any covid data
    elif update_query_time or update_query_name:

        temp = {"title": update_query_name[0], "content": update_query_time[0]}
        # lists which store the users inputs

        time_until_update = timeconversion.time_difference(update_query_time[0])

        # schedule_covid_updates(time_until_update, update_query_name[0])

        event_updates.append(temp)

        return render_template('index.html', title=data["keywords"]["title"], location=data["keywords"]["location"],
                               local_7day_infections=local_data["data"][1]["cumCasesBySpecimenDateRate"],
                               nation_location=data["keywords"]["national_location"],
                               national_7day_infections=national_data["data"][1]["cumCasesBySpecimenDateRate"],
                               hospital_cases=national_data["data"][1]["hospitalCases"],
                               deaths_total=national_data["data"][1]["cumDeaths60DaysByDeathDate"],
                               news_articles=news_API_request(), updates=event_updates)
    # renders the page with any updates that have been removed or added and scheduled


@app.route('/')
def index():
    return render_template('index.html', title=data["keywords"]["title"], location=data["keywords"]["location"],
                           local_7day_infections=local_data["data"][1]["cumCasesBySpecimenDateRate"],
                           nation_location=data["keywords"]["national_location"],
                           national_7day_infections=national_data["data"][1]["cumCasesBySpecimenDateRate"],
                           hospital_cases=national_data["data"][1]["hospitalCases"],
                           deaths_total=national_data["data"][1]["cumDeaths60DaysByDeathDate"],
                           news_articles=news_API_request(), updates=event_updates)
    # renders the template


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning('Errors will be logged to a file')
    run()
